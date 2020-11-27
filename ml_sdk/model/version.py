from dataclasses import dataclass
from distutils.version import LooseVersion

@dataclass
class ModelVersion:
    version: LooseVersion
