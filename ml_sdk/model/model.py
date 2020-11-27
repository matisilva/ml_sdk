from abc import ABCMeta, abstractmethod
from dataclasses import asdict
from ml_sdk.model.input import (
    InferenceInput,
    TrainInput,
    TestInput,
    InputType,
)
from ml_sdk.model.version import ModelVersion
from ml_sdk.model.output import (
    InferenceOutput,
    ReportOutput,
)


class MLModelInterface(metaclass=ABCMeta):

    def predict(self, input_: InferenceInput):
        input_ = self._preprocess(input_)
        output = self._predict(input_)
        output = self._postprocess(output)
        return asdict(output)

    def version(self):
        output = self._version()
        return asdict(output)

    def train(self, input_: TrainInput):
        output = self._train(input_)
        return output
        
    def test(self, input_: TestInput):
        output = self._test(input_)
        return output
    
    def deploy(self, input_: ModelVersion):
        output = self._deploy(input_)
        return output
    
    @abstractmethod
    def _deploy(self, version: ModelVersion):
        pass

    @abstractmethod
    def _preprocess(self, input_) -> InferenceInput:
        pass
    
    @abstractmethod
    def _predict(self, input_: InferenceInput):
        pass
    
    @abstractmethod
    def _postprocess(self, output) -> InferenceOutput:
        pass

    @abstractmethod
    def _train(self, input_: TrainInput) -> ModelVersion:
        pass

    @abstractmethod
    def _test(self, input_: TestInput, version: ModelVersion = None) -> ReportOutput:
        pass

    @abstractmethod
    def _version(self) -> ModelVersion:
        pass