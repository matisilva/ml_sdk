import json
from pydantic import BaseModel
from enum import Enum


class TextInput(BaseModel):
    text: str

class ImageInput(BaseModel):
    image: str # TODO numpy array

class Input(BaseModel):
    records: list
    batch_size: int = 1

class InferenceInput(Input):
    pass

class TestInput(Input):
    pass

class TrainInput(Input):
    pass
