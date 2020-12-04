from fastapi import APIRouter, HTTPException
from ml_sdk.communication.redis import RedisDispatcher, RedisSettings
from ml_sdk.io.input import TextInput
from ml_sdk.io.version import ModelVersion


class MLAPI:
    def __init__(self):
        if self.COMMUNICATION_TYPE == RedisDispatcher:
            self.settings = RedisSettings(topic=self.MODEL_NAME, host='redis')
        else:
            raise NotImplementedError
        self.connector = self.COMMUNICATION_TYPE(self.settings)
        self.router = APIRouter()
        self._add_routes()

    def _add_routes(self):
        self.router.add_api_route("/", self.index, methods=["GET"])
        self.router.add_api_route("/predict", self.post_predict, methods=["POST"])
        self.router.add_api_route("/version", self.get_version, methods=["GET"])
        self.router.add_api_route("/version", self.post_version, methods=["POST"])
        self.router.add_api_route("/train", self.get_train, methods=["GET"])
        self.router.add_api_route("/train", self.post_train, methods=["POST"])
        self.router.add_api_route("/test", self.get_test, methods=["GET"])
        self.router.add_api_route("/test", self.post_test, methods=["POST"])

    def post_predict(self, input_: TextInput):
        return self.connector.dispatch('predict', input_=input_.dict())

    def get_version(self):
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

    def index(self):
        return {"model": self.MODEL_NAME}