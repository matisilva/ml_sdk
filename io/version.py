from pydantic import BaseModel

class ModelVersion(BaseModel):
    version: str


class ModelDescription(BaseModel):
    model: str