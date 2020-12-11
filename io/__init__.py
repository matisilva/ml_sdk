from typing import List, Dict
from ml_sdk.io.input import (
    TextInput,
    ImageInput,
    InferenceInput,
    FileInput,
    Parameter,
)
from ml_sdk.io.version import ModelVersion, ModelDescription
from ml_sdk.io.output import (
    Output,
    InferenceOutput,
    ReportOutput,
    ClassificationOutput,
)


JobID = str

class TestJob(Output):
    job_id: JobID
    total: int
    processed: int = 0
    results: List[Dict] = []


class TrainJob(Output):
    job_id: JobID
    progress: int = 0
    scores: Dict = None
    version: ModelVersion = None


__all__ = [
    'FileInput',
    'TextInput',
    'ImageInput',
    'InferenceInput',
    'InferenceOutput',
    'ReportOutput',
    'ClassificationOutput',
    'ModelVersion',
    'ModelDescription',
    'TrainJob',
    'TestJob',
    'Parameter'
]
