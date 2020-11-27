from pydantic import BaseModel


class ClassificationOutput(BaseModel):
    prediction: str
    score: float

class Output(BaseModel):
    records: list
    scores: list

class InferenceOutput(Output):
    pass

class ReportOutput(Output):
    pass