import os
import json
import logging
from typing import List, Dict
from abc import ABCMeta, abstractmethod
from ml_sdk.communication.redis import RedisWorker, RedisSettings
from ml_sdk.io.input import (
    InferenceInput,
)
from ml_sdk.io.version import ModelVersion
from ml_sdk.io.output import (
    InferenceOutput,
    ReportOutput,
)


logger = logging.getLogger(__name__)


class MLServiceInterface(metaclass=ABCMeta):
    INPUT_TYPE = None
    OUTPUT_TYPE = None
    MODEL_NAME = None
    COMMUNICATION_TYPE = RedisWorker
    BINARY_FOLDER = "/bin/"
    VERSIONS_FILE = "versions.json"

    def __init__(self):
        # Validations
        self._validate_instance()

        # Communication setup
        if self.COMMUNICATION_TYPE == RedisWorker:
            self.settings = RedisSettings(topic=self.MODEL_NAME, host='redis')
        else:
            logger.error("Communication type not implemented")
            raise NotImplementedError

    def _read_config(self):
        with open(os.path.join(self.BINARY_FOLDER, self.VERSIONS_FILE)) as setup_file:
            content = json.load(setup_file)
        return content

    def _write_config(self, new_config):
        with open(os.path.join(self.BINARY_FOLDER, self.VERSIONS_FILE), "w") as setup_file:
            json.dump(new_config, setup_file, indent=4)

    def predict(self, input_: Dict) -> Dict:
        inference_input = self.INPUT_TYPE.preprocess(input_)
        inference_input = self.INPUT_TYPE(**input_)
        output = self._predict(inference_input)
        logger.info(f"Prediction {output}")
        return output.dict()

    def enabled_version(self) -> Dict:
        return self.version.dict()

    def available_versions(self) -> List[Dict]:
        config = self._read_config()
        return config

    def train_from_file(self, filename: str):
        logger.info(f"Parsing file {filename}")
        parser = self.FILE_PARSER()
        items = list(parser.parse(filename))
        logger.info(f"Updating metadata")
        for i in items:
            input_ = self.INPUT_TYPE.preprocess(i)
            i.update({
                "input": self.INPUT_TYPE(**input_)
            })
        items = [self.OUTPUT_TYPE(**reg).dict() for reg in items]
        self.train(items)

    def train(self, input_: List[Dict]) -> Dict:
        logger.info(f"Starting training")
        # Parse input
        train_input = [self.OUTPUT_TYPE(**i) for i in input_]

        # Launch train
        version = self._train(train_input)

        # Avail new version
        config = self._read_config()
        config["availables"].append(version.dict())
        self._write_config(config)
        logger.info(f"New version available {version}")
        return version.dict()

    def deploy(self, input_: Dict):
        self.version = ModelVersion(**input_)
        config = self._read_config()
        target_version = None
        for conf in config["availables"]:
            if conf["version"] == input_["version"]:
                target_version = ModelVersion(**conf)
                self._deploy(target_version)
                config["enabled"] = conf
                break
        self._write_config(config)
        logger.info(f"Version {target_version} succesfully deployed")
        return target_version

    @abstractmethod
    def _deploy(self, version: ModelVersion):
        pass

    @abstractmethod
    def _predict(self, inference_input: InferenceInput):
        pass

    @abstractmethod
    def _train(self, input_: List[InferenceInput]):
        pass

    def _validate_instance(self):
        assert self.INPUT_TYPE is not None, "You have to setup an INPUT_TYPE"
        assert self.OUTPUT_TYPE is not None, "You have to setup an OUTPUT_TYPE"
        assert self.COMMUNICATION_TYPE is not None, "You have to setup a COMMUNICATION_TYPE"
        assert self.MODEL_NAME is not None, "You have to setup a MODEL_NAME"

    def serve_forever(self):
        # Deploy enabled version
        config = self._read_config()
        self.version = ModelVersion(**config['enabled'])
        self._deploy(self.version)
        self.worker = self.COMMUNICATION_TYPE(self.settings, handler=self)
        logger.info(f"Initialized with version {self.version}")
        self.worker.serve_forever()
