from abc import ABCMeta, abstractmethod
from ml_sdk.io import BatchInferenceJob, JobID, InferenceOutput

class DatabaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_job(self, key: JobID) -> BatchInferenceJob:
        pass
    
    @abstractmethod
    def create_job(self, total: int) -> BatchInferenceJob:
        pass

    @abstractmethod
    def update_job(self, key: JobID, registry: InferenceOutput):
        pass
