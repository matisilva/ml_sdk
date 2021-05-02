import time
import msgpack
import logging
import redis
from dataclasses import dataclass
from typing import Iterable
from ml_sdk.communication import DispatcherInterface, WorkerInterface


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
        redis_pool = redis.ConnectionPool(**settings.conf)
        self.redis = redis.StrictRedis(connection_pool=redis_pool)
   
    @staticmethod
    def _decode(msg):
        return msgpack.unpackb(msg, use_list=False, raw=False)

    @staticmethod
    def _encode(msg):
        return msgpack.packb(msg, use_bin_type=True)

    def stop(self):
        self.stop = True

    def _set(self, key, message):
        self.redis.set(key, self._encode(message))

    def _get(self, key):
        while True:
            message = self.redis.get(key)
            if message is None:
                time.sleep(0.5)
                continue
            break
        message = self._decode(message)
        self.redis.delete(key)
        return message

    def _consume(self, key=None):
        if key:
            message = self._get(key)
        else:
            while True:
                # Read broadcasted messages
                message = self.pubsub.get_message()
                if message is not None:
                    if message['type'] == 'pmessage':
                        message = message['data']
                        break
                # Read individual messages
                message = self.redis.lpop(self.topic)
                if message is not None:
                    break
                time.sleep(0.5)
            message = self._decode(message)
            key = message.pop('key')
        return key, message

    def _load_input_data(self, **kwargs):
        input_ = kwargs.pop('input_', None)
        if not isinstance(input_, uuid.UUID):
            return {}
        items = self.redis.hvals(input_)
        self.redis.delete(input_)
        return {'input_': items}

    def _save_input_data(self, **kwargs):
        input_ = kwargs.pop('input_', None)
        if not isinstance(input_, Iterable):
            return {}
        key = uuid.uuid4()
        for i, value in enumerate(input_):
            self.redis.hset(key, i, value)
        return {'input_': key}


class RedisWorker(RedisNode, WorkerInterface):
    def __init__(self, settings: RedisSettings, handler):
        super(RedisWorker, self).__init__(settings)
        self.handler = handler
        self.pubsub = self.redis.pubsub()
        self.pubsub.psubscribe(f'{self.topic}*')
        self.pubsub.get_message()

    def _produce(self, message, key=None):
        self._set(key, message)

class RedisDispatcher(RedisNode, DispatcherInterface):

    def _produce(self, message, key=None):
        message['key'] = key
        self.redis.rpush(self.topic, self._encode(message))

    def _broadcast(self, message):
        message['key'] = None
        self.redis.publish(self.topic, self._encode(message))