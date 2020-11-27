import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict


class WorkerInterface(metaclass=ABCMeta):
    def _request(self):
        key, kwargs = self._consume()
        result = self._work(**kwargs)
        self._reply(key, result)
    
    def _work(self, *args, **kwargs):
        method = kwargs.pop('method', None)
        if method is None:
            return
        func = getattr(self.handler, method)
        return func(**kwargs)

    def _reply(self, key, message):
        self._produce(key, message)
    
    @abstractmethod
    def _produce(self, key, message):
        pass
    
    @abstractmethod
    def _consume(self):
        pass
    
    def serve(self):
        self.stop = False
        while not self.stop:
            self._request()


class DispatcherInterface(metaclass=ABCMeta):
    def dispatch(self, method, **kwargs):
        key = uuid.uuid4().hex
        kwargs['method'] = method
        self._produce(key, kwargs)
        result = self._get_result(key)
        return result
    
    def _get_result(self, key):
        key, result = self._consume(key)
        return result

    @abstractmethod
    def _produce(self, key, message):
        pass
    
    @abstractmethod
    def _consume(self, key=None):
        pass
