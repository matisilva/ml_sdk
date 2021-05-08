from abc import ABCMeta, abstractmethod
from ml_sdk.io import TestJob, TrainJob, JobID, JobID, InferenceOutput

class DatabaseInterface(metaclass=ABCMeta):
    @abstractmethod
    def get_test_job(self, job_id: JobID) -> TestJob:
        pass
    
    @abstractmethod
    def create_test_job(self, total: int) -> TestJob:
        pass

    @abstractmethod
    def update_test_job(self, job: TestJob, task: InferenceOutput):
        pass

    @abstractmethod
    def get_train_job(self, job_id: JobID) -> TrainJob:
        pass
    
    @abstractmethod
    def create_train_job(self, total: int) -> TrainJob:
        pass

    @abstractmethod
    def update_train_job(self, job: TrainJob, task: InferenceOutput):
        pass
