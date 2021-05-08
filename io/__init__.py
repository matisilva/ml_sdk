from typing import List, Dict
from ml_sdk.io.input import (
    TextInput,
    ImageInput,
    InferenceInput,
    FileInput,
)
from ml_sdk.io.version import ModelVersion, ModelDescription
from ml_sdk.io.output import (
    Output,
    InferenceOutput,
    ScoreOutput,
    ClassificationOutput,
    MultiClassificationOutput,
)


JobID = str

class Job(Output):
    job_id: JobID
    total: int
    processed: int = 0
    started_at: str = None
    end_at: str = None


class TestJob(Job):
    results: List[Dict] = []


class TrainJob(Job):
    version: ModelVersion = None


__all__ = [
    'FileInput',
    'TextInput',
    'ImageInput',
    'InferenceInput',
    'InferenceOutput',
    'ScoreOutput'
    'ClassificationOutput',
    'MultiClassificationOutput'
    'ModelVersion',
    'ModelDescription',
    'TrainJob',
    'TestJob',
]
