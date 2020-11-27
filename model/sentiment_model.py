from ml_sdk.model import MLModelInterface
from ml_sdk.model.input import (
    InferenceInput,
    TrainInput,
    TestInput
)
from ml_sdk.model.version import ModelVersion
from ml_sdk.model.output import ReportOutput, InferenceOutput
from AnalyseSentiment.AnalyseSentiment import AnalyseSentiment


class MLSentimentModel(MLModelInterface):
    def __init__(self):
        return self._deploy(version=None)

    def _deploy(self, version: ModelVersion):
        self.analyzer = AnalyseSentiment()

    def _preprocess(self, input_) -> InferenceInput:
        return InferenceInput(data=input_)
    
    def _predict(self, input_: InferenceInput):
        stats = self.analyzer.Analyse(input_.data)
        return stats
    
    def _postprocess(self, output) -> InferenceOutput:
        data = {
            'prediction': output['overall_sentiment'],
            'score': output['overall_sentiment_score']
        }
        return InferenceOutput(data=data)

    def _train(self, input_: TrainInput) -> ModelVersion:
        raise NotImplementedError

    def _test(self, input_: TestInput, version: ModelVersion) -> ReportOutput:
        raise NotImplementedError

    def _version(self) -> ModelVersion:
        return ModelVersion(version='unique')