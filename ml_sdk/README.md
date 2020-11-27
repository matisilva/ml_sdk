# TODO

```
from ml_sdk.communication.kafka import * 
kafka_settings = KafkaSettings(topic='users', dns='localhost', port=9093)
dispatcher = KafkaDispatcher(kafka_settings)
import random

class Model:
    def predict(self, **kwargs):
        print(kwargs)
        kwargs['response'] = random.choice(["positive", "negative"])
        return kwargs
worker = KafkaWorker(kafka_settings, Model())

worker.serve_forever()

dispatcher.dispatch(method='predict', another='something')



from ml_sdk.communication.redis import *
redis_settings = RedisSettings(topic='users', host='localhost')
dispatcher = RedisDispatcher(redis_settings)
import random

class Model:
    def predict(self, **kwargs):
        print(kwargs)
        kwargs['response'] = random.choice(["positive", "negative"])
        return kwargs
worker = RedisWorker(redis_settings, Model())

worker.serve_forever()

dispatcher.dispatch(method='predict', another='something')
```