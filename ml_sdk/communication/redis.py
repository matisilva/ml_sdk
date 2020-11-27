import time
import msgpack
import logging
import redis
from dataclasses import dataclass
from ml_sdk.communication import DispatcherInterface, WorkerInterface
from ml_sdk.model import MLModelInterface

logger = logging.getLogger(__name__)

@dataclass
class RedisSettings:
    topic: str
    host: str = 'redis'
    port: int = 6379
    db: int = 0

    @property
    def conf(self):
        return dict(host=self.host, db=self.db, port=self.port)


class RedisNode:
    def __init__(self, settings: RedisSettings):
        self.stop = False
        self.topic = settings.topic
        self.redis = redis.Redis(**settings.conf)
   
    @staticmethod
    def _decode(msg):
        return msgpack.unpackb(msg, use_list=False, raw=False)

    @staticmethod
    def _encode(msg):
        return msgpack.packb(msg, use_bin_type=True)

    def stop(self):
        self.stop = True

    def _consume(self, key=None):
        if key:
            while True:
                message = self.redis.get(key)
                if message is None:
                    time.sleep(0.5)
                    continue
                break
            message = self._decode(message)
            self.redis.delete(key)
        else:
            while True:
                message = self.redis.lpop(self.topic)
                if message is None:
                    time.sleep(0.5)
                    continue
                break
            message = self._decode(message)
            key = message.pop('key')
        return key, message


class RedisWorker(RedisNode, WorkerInterface):
    def __init__(self, settings: RedisSettings, handler: MLModelInterface):
        super(RedisWorker, self).__init__(settings)
        self.handler = handler

    def _produce(self, message, key=None):
        self.redis.set(key, self._encode(message))

class RedisDispatcher(RedisNode, DispatcherInterface):

    def _produce(self, message, key=None):
        message['key'] = key
        self.redis.rpush(self.topic, self._encode(message))
