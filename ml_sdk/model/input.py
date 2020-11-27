import json
from dataclasses import dataclass
from enum import Enum

class InputType(Enum):
    INFERENCE_MESSAGE = "inference"
    TRAIN_MESSAGE = "train"
    TEST_MESSAGE = "test"
    DEPLOY_MESSAGE = "deploy"


@dataclass
class Input:
    data: dict


@dataclass
class InferenceInput(Input):
    pass


@dataclass
class TestInput(Input):
    pass


@dataclass
class TrainInput(Input):
    pass
