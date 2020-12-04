import json
from pydantic import BaseModel
from enum import Enum



class Input(BaseModel):
    pass

class InferenceInput(Input):
    pass

class TestInput(BaseModel):
    pass

class TrainInput(BaseModel):
    pass

# Basic inference types
class TextInput(InferenceInput):
    text: str

class ImageInput(InferenceInput):
    image: str # TODO numpy array

class FileInput(InferenceInput):
    pass