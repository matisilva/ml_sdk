from ml_sdk.communication.kafka import KafkaWorker, KafkaSettings
from sentiment_model import MLSentimentModel

kafka_settings = KafkaSettings(topic='sentiment_model', dns='kafka')
worker = KafkaWorker(kafka_settings, handler=MLSentimentModel())

worker.serve()