import logging
import uuid
import pymongo
from dataclasses import dataclass
from datetime import datetime
from typing import Dict
from ml_sdk.database import DatabaseInterface
from ml_sdk.io import TestJob, TrainJob, JobID, InferenceOutput, ModelVersion


logger = logging.getLogger(__name__)


@dataclass
class MongoSettings:
    db: str
    host: str = 'mongo'
    port: int = 27017

    @property
    def conf(self):
        return dict(host=self.host, db=self.db, port=self.port)

    @property
    def url(self):
        return f'mongodb://{self.host}:{self.port}/'


class MongoDatabase(DatabaseInterface):
    def __init__(self, settings: MongoSettings):
        self.mongo = pymongo.MongoClient(settings.url)[settings.db]
        self.mongo_jobs = self.mongo['jobs']
        self.mongo_tasks = self.mongo['tasks']

    def get_test_job(self, job_id: JobID) -> TestJob:
        filter_ = {'job_id': job_id}
        job = self.mongo_jobs.find_one(filter_)
        job = TestJob(**job)
        job.results = list(self.mongo_tasks.find(filter_))
        job.processed = self.mongo_tasks.count_documents(filter_)
        return job

    def create_test_job(self, total: int) -> TestJob:
        job_id = uuid.uuid4()
        job = TestJob(
            job_id=JobID(job_id),
            total=total,
            started_at=str(datetime.now())
        )
        self.mongo_jobs.insert_one(job.dict())
        return job

    def update_test_job(self, job: TestJob, task: InferenceOutput):
        task.job_id = job.job_id
        self.mongo_tasks.insert_one(dict(task))

    def get_train_job(self, job_id: JobID) -> TrainJob:
        filter_ = {'job_id': job_id}
        job = self.mongo_jobs.find_one(filter_)
        return TrainJob(**job)

    def create_train_job(self) -> TrainJob:
        job_id = uuid.uuid4()
        job = TrainJob(
            job_id=JobID(job_id),
            total=100,
            started_at=str(datetime.now())
        )
        self.mongo_jobs.insert_one(dict(job))
        return job

    def update_train_job(self, job: TrainJob, version: ModelVersion):
        job.processed = job.total
        job.version = version
        job.end_at = str(datetime.now())
        filter_ = { "job_id": job.job_id }
        self.mongo_jobs.update_one(filter_, { "$set": dict(job) })
