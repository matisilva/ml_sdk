import time
import msgpack
import logging
import redis
import uuid
from typing import Dict
from ml_sdk.communication.redis import RedisSettings
from ml_sdk.database import DatabaseInterface
from ml_sdk.io import BatchInferenceJob, JobID, InferenceOutput, InferenceInput

logger = logging.getLogger(__name__)

class RedisDatabase(DatabaseInterface):
    def __init__(self, settings: RedisSettings):
        self.topic = settings.topic
        self.redis = redis.Redis(**settings.conf)

    @staticmethod
    def _decode(msg):
        return msgpack.unpackb(msg, use_list=False, raw=False)

    @staticmethod
    def _encode(msg):
        return msgpack.packb(msg, use_bin_type=True)

    def get_job(self, key: JobID) -> Dict:
        job = self._decode(self.redis.get(key))
        processed_keys = self.redis.keys(f"{self.topic}_{key}_*")
        results = self.redis.mget(processed_keys)
        job['results'] = [self._decode(r) for r in results]
        job['processed'] = len(results)
        return job

    def create_job(self, total: int) -> Dict:
        job_id = uuid.uuid4()
        job = {'job_id': JobID(job_id), 'total': total}
        self.redis.set(str(job_id), self._encode(job))
        return job

    def update_job(self, job: BatchInferenceJob, output: InferenceOutput):
        task_id = f"{self.topic}_{job.job_id}_{uuid.uuid4()}"
        self.redis.set(task_id, self._encode(output))
