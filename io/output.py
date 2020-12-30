from pydantic import BaseModel
from uuid import UUID
from typing import List, Dict


class Output(BaseModel):
    pass


class InferenceOutput(Output):
    input: Dict


class ReportOutput(Output):
    pass


# Basic output types
class Score(Output):
    score: float = 0


class Classification(Output):
    prediction: str


class ScoreOutput(InferenceOutput, Score):
    pass

class ClassificationOutput(InferenceOutput, Classification, Score):
    pass

class MultiClassificationOutput(ClassificationOutput):
    predictions: List[Classification] = []