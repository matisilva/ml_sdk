from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict


class Output(BaseModel):
    pass

class InferenceOutput(Output):
    pass

class ReportOutput(Output):
    pass


# Basic output types
class ClassificationOutput(InferenceOutput):
    prediction: str
    score: float
    input: Dict

# Batch Jobs
JobID = str


class BatchInferenceJob(Output):
    job_id: JobID
    total: int
    processed: int = 0
    results: List[Dict] = []