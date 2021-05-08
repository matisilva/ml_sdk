from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict, Union


class Output(BaseModel):
    pass


class InferenceOutput(Output):
    input: Dict
    job_id: str = None


class ReportOutput(Output):
    pass


# Basic output types
class Score(Output):
    score: float = 0


class Classification(Output):
    prediction: str


class ScoreOutput(InferenceOutput, Score):
    pass

class ScoredClassification(Classification, Score):
    pass

class ClassificationOutput(InferenceOutput, ScoredClassification):
    pass

class MultiClassificationOutput(ClassificationOutput):
    predictions: List[ScoredClassification] = []