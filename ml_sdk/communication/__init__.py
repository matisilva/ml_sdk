import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict


class WorkerInterface(metaclass=ABCMeta):
    def _request(self):
        key, kwargs = self._consume()
        method = kwargs.pop('method', None)
        result = self._execute(method, **kwargs)
        self._reply(key, result)
    
    def _execute(self, method, *args, **kwargs):
        func = getattr(self.handler, method)
        return func(**kwargs)

    def _reply(self, key, message):
        self._produce(message, key)   
    
    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self._request()

    def stop(self):
        self.stop = True

    @abstractmethod
    def _produce(self, message, key=None):
        pass
    
    @abstractmethod
    def _consume(self, key=None):
        pass

class DispatcherInterface(metaclass=ABCMeta):
    def dispatch(self, method, **kwargs):
        key = uuid.uuid4().hex
        kwargs['method'] = method
        self._produce(kwargs, key)
        result = self._get_result(key)
        return result
    
    def _get_result(self, key):
        key, result = self._consume(key)
        return result

    @abstractmethod
    def _produce(self, message, key=None):
        pass
    
    @abstractmethod
    def _consume(self, key=None):
        pass
