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
class Classification(Output):
    prediction: str
    score: float = 0


class ClassificationOutput(InferenceOutput, Classification):
    pass


class MultiClassificationOutput(ClassificationOutput):
    predictions: List[Classification] = []
