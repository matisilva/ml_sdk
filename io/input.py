import json
from fastapi import UploadFile
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

ImageInput = UploadFile
FileInput = UploadFile
