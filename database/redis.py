import time
import msgpack
import logging
import redis
import uuid
from datetime import datetime
from typing import Dict
from ml_sdk.communication.redis import RedisSettings
from ml_sdk.database import DatabaseInterface
from ml_sdk.io import TestJob, TrainJob, JobID, InferenceOutput, InferenceInput, ModelVersion


logger = logging.getLogger(__name__)


class RedisDatabase(DatabaseInterface):
    def __init__(self, settings: RedisSettings):
        self.topic = settings.topic
        redis_pool = redis.ConnectionPool(**settings.conf)
        self.redis = redis.StrictRedis(connection_pool=redis_pool)

    @staticmethod
    def _decode(msg):
        return msgpack.unpackb(msg, use_list=False, raw=False)

    @staticmethod
    def _encode(msg):
        return msgpack.packb(msg, use_bin_type=True)

    def get_test_job(self, job_id: JobID) -> TestJob:
        job = self._decode(self.redis.get(job_id))
        job = TestJob(**job)
        processed_keys = self.redis.keys(f"{self.topic}_{job_id}_*")
        results = self.redis.mget(processed_keys)
        job.results = [self._decode(r) for r in results]
        job.processed = len(results)
        return job

    def create_test_job(self, total: int) -> TestJob:
        job_id = uuid.uuid4()
        job = TestJob(
            job_id=JobID(job_id),
            total=total,
            started_at=str(datetime.now())
        )
        self.redis.set(str(job_id), self._encode(dict(job)))
        return job

    def update_test_job(self, job: TestJob, task: InferenceOutput):
        task_id = f"{self.topic}_{job.job_id}_{uuid.uuid4()}"
        self.redis.set(task_id, self._encode(task))

    def get_train_job(self, job_id: JobID) -> TrainJob:
        job = self._decode(self.redis.get(job_id))
        return TrainJob(**job)

    def create_train_job(self) -> TrainJob:
        job_id = uuid.uuid4()
        job = TrainJob(
            job_id=JobID(job_id),
            total=100,
            started_at=str(datetime.now())
        )
        self.redis.set(str(job_id), self._encode(dict(job)))
        return job

    def update_train_job(self, job: TrainJob, version: ModelVersion):
        job_id = job.job_id
        job = self.get_train_job(job_id)
        job.processed = job.total
        job.version = version
        job.end_at = str(datetime.now())
        self.redis.set(str(job_id), self._encode(dict(job)))
