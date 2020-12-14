from typing import List, Dict
from abc import ABCMeta, abstractmethod
from ml_sdk.communication.redis import RedisWorker, RedisSettings
from ml_sdk.io.input import (
    InferenceInput,
)
from ml_sdk.io.version import ModelVersion
from ml_sdk.io.output import (
    InferenceOutput,
    ReportOutput,
)


class MLServiceInterface(metaclass=ABCMeta):
    INPUT_TYPE = None
    OUTPUT_TYPE = None
    MODEL_NAME = None
    COMMUNICATION_TYPE = RedisWorker
    INITIAL_VERSION = ModelVersion(version="Default")

    def __init__(self):
        self._validate_instance()
        if self.COMMUNICATION_TYPE == RedisWorker:
            self.settings = RedisSettings(topic=self.MODEL_NAME, host='redis')
        else:
            raise NotImplementedError
        self.worker = self.COMMUNICATION_TYPE(self.settings, handler=self)
        self._deploy(self.INITIAL_VERSION)
    
    def _validate_instance(self):
        assert self.INPUT_TYPE is not None, "You have to setup an INPUT_TYPE"
        assert self.OUTPUT_TYPE is not None, "You have to setup an OUTPUT_TYPE"
        assert self.COMMUNICATION_TYPE is not None, "You have to setup a COMMUNICATION_TYPE"
        assert self.MODEL_NAME is not None, "You have to setup a MODEL_NAME"

    def serve_forever(self):
        self.worker.serve_forever()

    def predict(self, input_: Dict):
        inference_input = self.INPUT_TYPE(**input_)
        output = self._predict(inference_input)
        return output.dict()

    def version(self):
        output = self._version()
        return output.dict()

    def train(self, input_: List[Dict]):
        train_input = [self.OUTPUT_TYPE(**i) for i in input_]
        output = self._train(train_input)
        return output.dict()
    
    def deploy(self, input_: Dict):
        self._deploy(ModelVersion(**input_))
        return self.version()
    
    @abstractmethod
    def _deploy(self, version: ModelVersion):
        pass

    @abstractmethod
    def _predict(self, inference_input: InferenceInput):
        pass

    @abstractmethod
    def _train(self, input_: List[InferenceInput]):
        pass

    @abstractmethod
    def _version(self):
        pass