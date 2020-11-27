from sentiment_model import MLSentimentModel
from ml_sdk.communication.redis import RedisWorker, RedisSettings

redis_settings = RedisSettings(topic='sentiment_model', host='redis')
worker = RedisWorker(redis_settings, handler=MLSentimentModel())

worker.serve_forever()