from ml_sdk.communication.kafka import KafkaRPCWorker, KafkaSettings
from sentiment_model import MLSentimentModel

kafka_settings = KafkaSettings(topic='sentiment_model', dns='kafka')
worker = KafkaRPCWorker(kafka_settings, handler=MLSentimentModel())

worker.listen()