from typing import Dict
from ml_sdk.model import MLModelInterface
from ml_sdk.model.input import (
    InferenceInput,
    TrainInput,
    TestInput,
    TextInput
)
from ml_sdk.model.version import ModelVersion
from ml_sdk.model.output import ReportOutput, InferenceOutput, ClassificationOutput
from AnalyseSentiment.AnalyseSentiment import AnalyseSentiment


class MLSentimentModel(MLModelInterface):
    def __init__(self):
        return self._deploy(version=None)

    def _deploy(self, version: ModelVersion):
        self.analyzer = AnalyseSentiment()

    def _preprocess(self, input_: Dict) -> InferenceInput:
        return TextInput(**input_)
    
    def _predict(self, input_: InferenceInput):
        stats = self.analyzer.Analyse(input_.text)
        return stats
    
    def _postprocess(self, output) -> InferenceOutput:
        print(output)
        data = {
            'prediction': output['overall_sentiment'],
            'score': output['overall_sentiment_score']
        }
        return ClassificationOutput(**data)

    def _train(self, input_: TrainInput) -> ModelVersion:
        raise NotImplementedError

    def _test(self, input_: TestInput, version: ModelVersion) -> ReportOutput:
        raise NotImplementedError

    def _version(self) -> ModelVersion:
        return ModelVersion(version='unique')