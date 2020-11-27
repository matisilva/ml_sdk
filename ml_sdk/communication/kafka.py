import json
from dataclasses import dataclass
from kafka_rpc import KRPCServer, KRPCClient
from typing import Dict
from ml_sdk.communication import RPCDispatcherInterface, RPCWorkerInterface
from ml_sdk.model import MLModelInterface

@dataclass
class KafkaSettings:
    topic: str
    dns: str
    port: int = '9092'


class KafkaRPCWorker(RPCWorkerInterface):
    def __init__(self, settings: KafkaSettings, handler: MLModelInterface):
        self.topic = settings.topic
        self.server_uri = f'{settings.dns}:{settings.port}'
        self.handler = handler
        self.rpc = KRPCServer(self.server_uri, handle=self.handler, topic_name=self.topic)


class KafkaRPCDispatcher(RPCDispatcherInterface):
    def __init__(self, settings: KafkaSettings):
        self.topic = settings.topic
        self.server_uri = f'{settings.dns}:{settings.port}'
        self.rpc = KRPCClient(self.server_uri, topic_name=self.topic)