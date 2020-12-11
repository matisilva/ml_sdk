from typing import Dict, Any, List
import json
from fastapi import UploadFile
from pydantic import BaseModel
from enum import Enum


class Parameter(BaseModel):
    key: str
    value: str


ParametersInput = List[Parameter]


class Input(BaseModel):
    pass


class InferenceInput(Input):
    pass


# Basic inference types
class TextInput(InferenceInput):
    text: str

ImageInput = UploadFile
FileInput = UploadFile
