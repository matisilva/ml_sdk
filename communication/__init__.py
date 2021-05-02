import uuid
from abc import ABCMeta, abstractmethod
from typing import Dict


class WorkerInterface(metaclass=ABCMeta):
    def _listen(self):
        key, kwargs = self._consume()
        method = kwargs.pop('method', None)
        kwargs.update(self._load_input_data(**kwargs))
        result = self._execute(method, **kwargs)
        if key:
            self._set_reply(key, result)

    def _execute(self, method, *args, **kwargs):
        func = getattr(self.handler, method)
        return func(**kwargs)

    def _set_reply(self, key, message):
        self._produce(message, key)
    
    def serve_forever(self):
        self.stop = False
        while not self.stop:
            self._listen()

    def stop(self):
        self.stop = True

    @abstractmethod
    def _produce(self, message, key=None):
        pass
    
    @abstractmethod
    def _consume(self, key=None):
        pass

    def _load_input_data(self, **kwargs):
        return {}


class DispatcherInterface(metaclass=ABCMeta):
    def dispatch(self, method, **kwargs):
        key = uuid.uuid4().hex
        kwargs['method'] = method
        kwargs.update(self._save_input_data(**kwargs))
        self._produce(kwargs, key)
        result = self._get_reply(key)
        return result

    def broadcast(self, method, **kwargs):
        kwargs['method'] = method
        return self._broadcast(kwargs)

    def _get_reply(self, key):
        key, result = self._consume(key)
        return result

    @abstractmethod
    def _produce(self, message, key=None):
        pass

    @abstractmethod
    def _broadcast(self, message):
        pass
    
    @abstractmethod
    def _consume(self, key=None):
        pass

    def _save_input_data(self, **kwargs):
        return {}
