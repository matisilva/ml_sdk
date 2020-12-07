from pydantic import BaseModel



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