from ml_sdk.communication.redis import RedisDispatcher, RedisSettings
from ml_sdk.io.input import TextInput
from ml_sdk.io.output import ClassificationOutput
from ml_sdk.api import MLAPI


class SentimentAnalysisAPI(MLAPI):
    MODEL_NAME = 'sentiment_analysis'
    INPUT_TYPE = TextInput
    OUTPUT_TYPE = ClassificationOutput
    COMMUNICATION_TYPE = RedisDispatcher

