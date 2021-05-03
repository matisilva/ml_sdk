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

    def get_job(self, key: JobID) -> Dict:
        filter_ = {'job_id': key}
        job = self.mongo_jobs.find_one(filter_)
        job['results'] = list(self.mongo_tasks.find(filter_))
        job['processed'] = self.mongo_tasks.count_documents(filter_)
        return job

    def create_job(self, total: int) -> Dict:
        job_id = uuid.uuid4()
        job = {'job_id': JobID(job_id), 'total': total, 'started_at': str(datetime.now())}
        self.mongo_jobs.insert_one(job)
        return job

    def update_job(self, job: TestJob, output: InferenceOutput):
        task = dict(output)
        task['job_id'] = job.job_id
        self.mongo_tasks.insert_one(task)

    def get_train_job(self, key: JobID) -> Dict:
        job = self.mongo_jobs.find_one({ "job_id": key })
        return job

    def create_train_job(self) -> Dict:
        job_id = uuid.uuid4()
        job = {'job_id': JobID(job_id), 'progress': 0, 'started_at': str(datetime.now())}
        self.mongo_jobs.insert_one(job)
        return job

    def update_train_job(self, job: TrainJob, version: ModelVersion):
        job_patch = {'progress': 100, 'version': version}
        self.mongo_jobs.update_one({ "job_id": job.job_id }, { "$set": job_patch })
