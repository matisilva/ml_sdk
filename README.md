# FaMAF sample deployment platform
This code deploys a set of models with its needed infrastructure.
It is using [ML_SDK](https://bitbucket.org/vinculacion-famaf-rentas/ml_sdk) as a submodule.

## Arch overview
![Arch overview](https://bitbucket.org/vinculacion-famaf-rentas/sample_deployment_platform/raw/2140614ef3ba683cd41cdd91d0f69c8c0b216a5a/ML%20SDK.jpg "Architecture overview")

This is the list of models to be deployed:
    - SentimentAnalysis - Python - unique version

## How to clone the repo?
**IMPORTANT**: clone the repo with its submodules just as follows

```
git clone --recurse-submodules git@bitbucket.org:vinculacion-famaf-rentas/sample_deployment_platform.git
```

To update SDK (pull submodules)

```
git submodule update
```

## How to run the repo:
Install docker and docker-compose and then just run
```
docker-compose up -d
```
## Interaction

### API Documentation
Documentation available in `http://localhost/redoc`

### Interact with the models
Swagger available in `http://localhost/docs`
Check **Try it out** button in each definition.

## Traefik as a load balancer:
TODO

## How to add your models?
Please fork from this repo and follow the steps
1) create a new folder copying from `./model` folder as a template.
2) modify `service.py` file adding your customizations for the model just inheriting from `MLServiceInterface`
```python
from ml_sdk.service import MLServiceInterface
from ml_sdk.io.input import (
    InferenceInput,
    TrainInput,
    TestInput,
    TextInput
)
from ml_sdk.io.version import ModelVersion
from ml_sdk.io.output import ReportOutput, ClassificationOutput
from ml_sdk.communication.redis import RedisWorker, RedisSettings
from AnalyseSentiment.AnalyseSentiment import AnalyseSentiment

class MyNewModel(MLServiceInterface):
    MODEL_NAME = 'my_new_model'
    INPUT_TYPE = TextInput
    OUTPUT_TYPE = ClassificationOutput
    COMMUNICATION_TYPE = RedisWorker
    INITIAL_VERSION = None
    
    def _deploy(self, version: ModelVersion):
        ...
    
    def _predict(self, input_: TextInput) -> ClassificationOutput:
        ...

    def _train(self, input_: TrainInput) -> ModelVersion:
        ...
 
    def _test(self, input_: TestInput, version: ModelVersion) -> ReportOutput:
        ...

    def _version(self) -> ModelVersion:
        ...

if __name__ == '__main__':
    MyNewModel().serve_forever()
```
3) add inside `./api/routers` your routes in a separate file just coping `./api/routers/sentiment_analyisis.py` as a template.
4) add your model in mapping placed at`./api/routers/__init__.py` as follows
```python
...
from routers.my_new_model import MyNewModelAPI

MODELS_TO_DEPLOY = [
    ...
    MyNewModelAPI
]
```
5) Finally add your new service in the `docker-compose.yml` file
```yaml
  <MY_MODEL_NAME>:
    image: <MY_MODEL_NAME>
    build:
      context: ./
      dockerfile: ./<MY_MODEL_NAME>/Dockerfile
    tty: true
```