from fastapi import APIRouter, HTTPException, File
from typing import List
from ml_sdk.communication.redis import RedisDispatcher, RedisSettings
from ml_sdk.io import FileInput
from ml_sdk.io import InferenceOutput, InferenceInput
from ml_sdk.io.version import ModelVersion, ModelDescription


class MLAPI:
    MODEL_NAME = None
    FILE_PARSER = None
    COMMUNICATION_TYPE = None
    INPUT_TYPE = None
    OUTPUT_TYPE = None

    def __init__(self):
        self._validate_instance()
        if self.COMMUNICATION_TYPE == RedisDispatcher:
            self.settings = RedisSettings(topic=self.MODEL_NAME, host='redis')
        else:
            raise NotImplementedError
        self.connector = self.COMMUNICATION_TYPE(self.settings)
        self.router = APIRouter()
        self._add_routes()

    def _validate_instance(self):
        assert self.INPUT_TYPE is not None, "You have to setup an INPUT_TYPE"
        assert self.OUTPUT_TYPE is not None, "You have to setup an OUTPUT_TYPE"
        assert self.COMMUNICATION_TYPE is not None, "You have to setup a COMMUNICATION_TYPE"
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
            self.router.add_api_route("/predict_from_file",
                                      self.post_predict_from_file,
                                      methods=["POST"],
                                      response_model= List[self.OUTPUT_TYPE])
        self.router.add_api_route("/version",
                                  self.get_version,
                                  methods=["GET"]
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

    def post_predict_from_file(self, input_: FileInput = File(...)) -> List[InferenceOutput]:
        assert callable(self.FILE_PARSER), "You have to setup first a FILE_PARSER"
        parser = self.FILE_PARSER()
        parsed_content = parser.parse(input_.file)
        return [self.post_predict(self.INPUT_TYPE(**registry)) for registry in parsed_content]

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