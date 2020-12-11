from abc import ABCMeta, abstractmethod
from ml_sdk.io import JobID, InferenceOutput

class DatabaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_job(self, key: JobID):
        pass
    
    @abstractmethod
    def create_job(self, total: int):
        pass

    @abstractmethod
    def update_job(self, key: JobID, registry: InferenceOutput):
        pass
