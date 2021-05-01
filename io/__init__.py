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

class TestJob(Output):
    job_id: JobID
    total: int
    processed: int = 0
    started_at: str = None
    results: List[Dict] = []


class TrainJob(Output):
    job_id: JobID
    progress: int = 0
    started_at: str = None
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
