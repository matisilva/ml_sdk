from abc import ABCMeta, abstractmethod
from typing import Dict


class RPCWorkerInterface(metaclass=ABCMeta):
    def listen(self):
        self.rpc.server_forever()

class RPCDispatcherInterface(metaclass=ABCMeta):
    def dispatch(self, method, **kwargs):
        func = getattr(self.rpc, method)
        return func(**kwargs)
