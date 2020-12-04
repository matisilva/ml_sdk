from abc import ABCMeta, abstractmethod
from ml_sdk.communication.redis import RedisWorker, RedisSettings
from ml_sdk.io.input import (
    InferenceInput,
    TrainInput,
    TestInput,
)
from ml_sdk.io.version import ModelVersion
from ml_sdk.io.output import (
    InferenceOutput,
    ReportOutput,
)


class MLServiceInterface(metaclass=ABCMeta):
    def __init__(self):
        if self.COMMUNICATION_TYPE == RedisWorker:
            self.settings = RedisSettings(topic=self.MODEL_NAME, host='redis')
        else:
            raise NotImplementedError
        self.worker = self.COMMUNICATION_TYPE(self.settings, handler=self)
        self._deploy(self.INITIAL_VERSION)
    
    def serve_forever(self):
        self.worker.serve_forever()

    def predict(self, input_: InferenceInput):
        inference_input = self.INPUT_TYPE(**input_)
        output = self._predict(inference_input)
        return output.dict()

    def version(self):
        output = self._version()
        return output.dict()

    def train(self, _input: TrainInput):
        # TODO call this async in a thread and return a default output
        output = self._train(_input)
        return output
        
    def test(self, input_: TestInput):
        # TODO call this async in a thread and return a default output
        output = self._test(input_)
        return output
    
    def deploy(self, input_: ModelVersion):
        output = self._deploy(input_)
        return output
    
    @abstractmethod
    def _deploy(self, version: ModelVersion):
        pass

    @abstractmethod
    def _predict(self, inference_input: InferenceInput):
        pass

    @abstractmethod
    def _train(self, train_input: TrainInput) -> ModelVersion:
        pass

    @abstractmethod
    def _test(self, test_input: TestInput, version: ModelVersion = None) -> ReportOutput:
        pass

    @abstractmethod
    def _version(self) -> ModelVersion:
        pass