import logging
from fastapi import APIRouter, File, status
from fastapi.responses import StreamingResponse, JSONResponse
from typing import List, Dict
from ml_sdk.api.parsers import CSVFileParser
from ml_sdk.communication.redis import RedisDispatcher, RedisSettings
from ml_sdk.database.redis import RedisDatabase
from ml_sdk.io import (
    FileInput,
    InferenceOutput,
    InferenceInput,
    TestJob,
    TrainJob,
    JobID,
)
from ml_sdk.io.version import ModelVersion, ModelDescription, VersionID


logger = logging.getLogger()


class MLAPI:
    MODEL_NAME = None
    DESCRIPTION = None
    INPUT_TYPE = None
    OUTPUT_TYPE = None
    COMMUNICATION_TYPE = RedisDispatcher
    DATABASE_TYPE = RedisDatabase
    FILE_PARSER = CSVFileParser

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
        self.router.add_api_route("/",
                                  self.index,
                                  methods=["GET"],
                                  response_model=ModelDescription)
        self.router.add_api_route("/predict",
                                  self.post_predict(),
                                  methods=["POST"],
                                  response_model=self.OUTPUT_TYPE)
        self.router.add_api_route("/test",
                                  self.post_test,
                                  methods=["POST"],
                                  response_model=TestJob)
        self.router.add_api_route("/test/{job_id}",
                                  self.get_test,
                                  methods=["GET"],
                                  response_model=TestJob)
        self.router.add_api_route("/train",
                                  self.post_train,
                                  methods=["POST"],
                                  response_model=TrainJob)
        self.router.add_api_route("/train/{job_id}",
                                  self.get_train,
                                  methods=["GET"],
                                  response_model=TrainJob)
        self.router.add_api_route("/version/{version_id}",
                                  self.post_version,
                                  methods=["POST"],
                                  response_model=ModelVersion)
        self.router.add_api_route("/version",
                                  self.get_version,
                                  methods=["GET"])

    # VIEWS
    def post_predict(self):
        connector = self.connector
        def _inner(input_: self.INPUT_TYPE) -> self.OUTPUT_TYPE:
            results = connector.dispatch('predict', input_=input_.dict())
            return results
        return _inner

    def get_test(self, job_id: JobID, as_file: bool = False) -> TestJob:
        # Job results
        job_result = self.database.get_job(JobID(job_id))
        job_result['results'] = [self.OUTPUT_TYPE(**res) for res in job_result['results']]
        
        # Return file or formatted repsonse
        if as_file:
            return self._get_test_file(job_result)
        else:
            return self._get_test(job_result)

    def post_test(self, input_: FileInput = File(...)) -> TestJob:
        assert callable(self.FILE_PARSER), "You have to setup first a FILE_PARSER"

        # parsing
        parser = self.FILE_PARSER()
        items = parser.parse(input_.file)
        items = list(items)

        # job creation
        job = self.database.create_job(total=len(items))
        job = TestJob(**job)

        # trigger tasks
        self._async_predict(job=job, items=items)
        return job
    
    def get_train(self, job_id: JobID) -> TrainJob:
        job_result = self.database.get_train_job(JobID(job_id))
        return TrainJob(**job_result)

    def post_train(self, input_: FileInput = File(...)) -> TrainJob:
        assert callable(self.FILE_PARSER), "You have to setup first a FILE_PARSER"

        # parsing
        parser = self.FILE_PARSER()
        items = list(parser.parse(input_.file)) # TODO consume 1 by 1
        try:
            for i in items:
                i.update({
                    "input": {
                        k: i[k]
                        for k in self.INPUT_TYPE.__fields__
                    }
                })
            items = [self.OUTPUT_TYPE(**reg).dict() for reg in items]
        except Exception as exc:
            return JSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=jsonable_encoder({"detail": exc.errors(), "Error": "Input file corrupt"}),
            )

        # job creation
        job = self.database.create_train_job()
        job = TrainJob(**job)

        # trigger train task
        self._async_train(job=job, items=items)
        return job

    def get_version(self) -> ModelVersion:
        return self.connector.dispatch('available_versions')

    def post_version(self, version_id: VersionID):
        input_ = ModelVersion(version=version_id)
        self.connector.broadcast('deploy', input_=input_.dict())
        return input_

    def index(self) -> ModelDescription:
        return ModelDescription(**{"model": self.MODEL_NAME,\
                                   "description": self.DESCRIPTION,
                                   "version": self.connector.dispatch('enabled_version')})

    # INTERNAL
    def _get_test_file(self, job_result: TestJob):
        filename = self.FILE_PARSER.generate_filename(prefix=self.MODEL_NAME)
        media_type = self.FILE_PARSER.mediatype
        lines = job_result['results']
        with self.FILE_PARSER.build(lines=lines) as file_content:
            response = StreamingResponse(file_content,
                                         media_type=media_type)
            response.headers["Content-Disposition"] = f"attachment; filename={filename}"
        return response

    def _get_test(self, job_result: TestJob):
        return TestJob(**job_result)

    def _async_predict(self, job: TestJob, items: List):
        # TODO refactor this controlling threads.
        import threading
        def _inner(database, job, item):
            predict_func = self.post_predict()
            try:
                item = self.INPUT_TYPE(**item)
            except Exception as e:
                logger.info(f"Ommited {item} Failure during parsing: {str(e)}")
            else:
                inference_result = predict_func(item)
                self.database.update_job(job=job, output=inference_result)
        for item in items:
            t = threading.Thread(target=_inner, args=(self.database, job, item))
            t.start()


    def _async_train(self, job: TestJob, items: List):
        # TODO refactor this controlling threads.
        import threading
        def _inner(database, job, items):
            model_version = self.connector.dispatch('train', input_=items)
            self.database.update_train_job(job=job, version=model_version)

        t = threading.Thread(target=_inner, args=(self.database, job, items))
        t.start()