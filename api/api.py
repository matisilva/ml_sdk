from fastapi import APIRouter, HTTPException, File
from typing import List
from ml_sdk.communication.redis import RedisDispatcher, RedisSettings
from ml_sdk.database.redis import RedisDatabase
from ml_sdk.io import FileInput
from ml_sdk.io import InferenceOutput, InferenceInput, BatchInferenceJob, JobID
from ml_sdk.io.version import ModelVersion, ModelDescription


class MLAPI:
    MODEL_NAME = None
    FILE_PARSER = None
    COMMUNICATION_TYPE = None
    DATABASE_TYPE = None
    INPUT_TYPE = None
    OUTPUT_TYPE = None

    def __init__(self):
        self._validate_instance()
        # Communication
        if self.COMMUNICATION_TYPE == RedisDispatcher:
            comm_settings = RedisSettings(topic=self.MODEL_NAME, host='redis')
        else:
            raise NotImplementedError
        self.connector = self.COMMUNICATION_TYPE(comm_settings)

        # Database
        if self.DATABASE_TYPE == RedisDatabase:
            db_settings = RedisSettings(topic=f"{self.MODEL_NAME}_jobs", host='redis')
        else:
            raise NotImplementedError
        self.database = self.DATABASE_TYPE(db_settings)

        # API Routes
        self.router = APIRouter()
        self._add_routes()

    def _validate_instance(self):
        assert self.INPUT_TYPE is not None, "You have to setup an INPUT_TYPE"
        assert self.OUTPUT_TYPE is not None, "You have to setup an OUTPUT_TYPE"
        assert self.COMMUNICATION_TYPE is not None, "You have to setup a COMMUNICATION_TYPE"
        assert self.DATABASE_TYPE is not None, "You have to setup a DATABASE_TYPE"
        assert self.MODEL_NAME is not None, "You have to setup a MODEL_NAME"

    def _add_routes(self):
        self.router.add_api_route("/", self.index,
                                  methods=["GET"],
                                  response_model=ModelDescription)
        self.router.add_api_route("/predict",
                                  self.post_predict(),
                                  methods=["POST"],
                                  response_model=self.OUTPUT_TYPE)
        if self.FILE_PARSER is not None:
            self.router.add_api_route("/batch_predict",
                                      self.post_batch_predict,
                                      methods=["POST"],
                                      response_model=BatchInferenceJob)
            self.router.add_api_route("/batch_predict",
                                      self.get_batch_predict,
                                      methods=["GET"],
                                      response_model=BatchInferenceJob)
        self.router.add_api_route("/version",
                                  self.get_version,
                                  methods=["GET"],
                                  response_model=ModelVersion)
        self.router.add_api_route("/version",
                                  self.post_version,
                                  methods=["POST"],
                                  response_model=ModelVersion)
        # TODO complete response model
        self.router.add_api_route("/train",
                                  self.get_train,
                                  methods=["GET"])
        self.router.add_api_route("/train",
                                  self.post_train,
                                  methods=["POST"])
        self.router.add_api_route("/test",
                                  self.get_test,
                                  methods=["GET"])
        self.router.add_api_route("/test",
                                  self.post_test,
                                  methods=["POST"])

    def post_predict(self):
        connector = self.connector
        def _inner(input_: self.INPUT_TYPE) -> self.OUTPUT_TYPE:
            return connector.dispatch('predict', input_=input_.dict())
        return _inner

    def post_batch_predict(self, input_: FileInput = File(...)) -> BatchInferenceJob:
        assert callable(self.FILE_PARSER), "You have to setup first a FILE_PARSER"

        # parsing
        parser = self.FILE_PARSER()
        parsed_content = parser.parse(input_.file)
        items = [self.INPUT_TYPE(**registry) for registry in parsed_content]

        # job creation
        job = self.database.create_job(total=len(items))
        job = BatchInferenceJob(**job)
        # trigger tasks
        self.async_predict(job=job, items=items)
        return job

    def async_predict(self, job: BatchInferenceJob, items: List[InferenceInput]):
        # TODO refactor this controlling threads.
        import threading
        def _inner(database, job, item):
            predict_func = self.post_predict()
            inference_result = predict_func(item)
            self.database.update_job(job=job, output=inference_result)
        for item in items:
            t = threading.Thread(target=_inner, args=(self.database, job, item))
            t.start()

    def get_batch_predict(self, job_id: JobID) -> BatchInferenceJob:
        job_result = self.database.get_job(JobID(job_id))
        job_result['results'] = [self.OUTPUT_TYPE(**res) for res in job_result['results']]
        return BatchInferenceJob(**job_result)

    def get_version(self) -> ModelVersion:
        return self.connector.dispatch('version')

    def post_version(self, input_: ModelVersion):
        raise HTTPException(status_code=404, detail="Not Implemented")

    def get_train(self):
        raise HTTPException(status_code=404, detail="Not Implemented")

    def post_train(self):
        raise HTTPException(status_code=404, detail="Not Implemented")

    def get_test(self):
        raise HTTPException(status_code=404, detail="Not Implemented")

    def post_test(self):
        raise HTTPException(status_code=404, detail="Not Implemented")

    def index(self) -> ModelDescription:
        return ModelDescription(**{"model": self.MODEL_NAME})