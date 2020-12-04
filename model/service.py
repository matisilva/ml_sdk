from ml_sdk.service import MLServiceInterface
from ml_sdk.io.input import (
    InferenceInput,
    TrainInput,
    TestInput,
    TextInput
)
from ml_sdk.io.version import ModelVersion
from ml_sdk.io.output import ReportOutput, ClassificationOutput
from ml_sdk.communication.redis import RedisWorker, RedisSettings
from AnalyseSentiment.AnalyseSentiment import AnalyseSentiment

class MLSentimentModel(MLServiceInterface):
    MODEL_NAME = 'sentiment_analysis'
    INPUT_TYPE = TextInput
    OUTPUT_TYPE = ClassificationOutput
    COMMUNICATION_TYPE = RedisWorker
    INITIAL_VERSION = None
    
    def _deploy(self, version: ModelVersion):
        self.analyzer = AnalyseSentiment()
    
    def _predict(self, input_: TextInput) -> ClassificationOutput:
        stats = self.analyzer.Analyse(input_.text)
        output = {
            'prediction': stats['overall_sentiment'],
            'score': stats['overall_sentiment_score']
        }
        return self.OUTPUT_TYPE(**output)

    def _train(self, input_: TrainInput) -> ModelVersion:
        raise NotImplementedError

    def _test(self, input_: TestInput, version: ModelVersion) -> ReportOutput:
        raise NotImplementedError

    def _version(self) -> ModelVersion:
        output = {
            'version': 'unique',
        }
        return ModelVersion(**output)

if __name__ == '__main__':
    MLSentimentModel().serve_forever()