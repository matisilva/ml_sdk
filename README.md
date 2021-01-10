# FaMAF SDK
This is a set of tools to make the deployment of ML models easier.

## Arch overview
![Arch overview](./ML%20SDK.jpg "Architecture overview")

## API (dispatcher): FastAPI
You just need to create a FastAPI instance and add your model routes there.
```
app = FastAPI(
    title=title,
    description=description,
    version=version,
)

MODELS_TO_DEPLOY = [
    SentimentAnalisisAPI,
    ClassifierAPI,
]

for model in MODELS_TO_DEPLOY:
    model = model()
    app.include_router(model.router,
                       prefix=f"/{model.MODEL_NAME}",
                       tags=[model.MODEL_NAME])
```

To build the models you can just inherit from the SDK as follows:
```
from enum import Enum
from ml_sdk.communication.redis import RedisDispatcher
from ml_sdk.database.redis import RedisDatabase
from ml_sdk.io import InferenceInput, MultiClassificationOutput
from ml_sdk.api import MLAPI, CSVFileParser, XLSXFileParser


class Channel(str, Enum):
    web = "Pagina web"
    redes = "Redes"
    telefonico = "Telefonico"
    chat = "Chat"

class CommentsInput(InferenceInput):
    comentario_atencion: str
    comentario_fcr: str
    comentario_canal: str
    comentario_ce: str
    canal: Channel


class ClassifierAPI(MLAPI):
    MODEL_NAME = 'classifier'
    INPUT_TYPE = CommentsInput
    OUTPUT_TYPE = MultiClassificationOutput
    FILE_PARSER = XLSXFileParser
```

## MLModel (worker): Python
You just need to inherit from SDK and implement some methods from the interface.
```
# Python imports
import logging
from typing import List
from enum import Enum

# Lib imports
from fasttext import load_model
from ml_sdk.service import MLServiceInterface
from ml_sdk.io.input import InferenceInput
from ml_sdk.io.version import ModelVersion, Scores
from ml_sdk.io.output import MultiClassificationOutput, InferenceOutput
from ml_sdk.communication.redis import RedisWorker


logger = logging.getLogger(__name__)


class Channel(str, Enum):
    web = "Pagina web"
    redes = "Redes"
    telefonico = "Telefonico"
    chat = "Chat"


class CommentsInput(InferenceInput):
    comentario_atencion: str
    comentario_fcr: str
    comentario_canal: str
    comentario_ce: str
    canal: Channel

    @property
    def text(self):
        return " ".join([getattr(self, f) for f in self.__fields__])

    @property
    def preprocessed_text(self):
        return (self.text
                .lower()
                .replace("\r", " ")
                .replace("\n", " "))


class Classifier(MLServiceInterface):
    MODEL_NAME = 'classifier'
    INPUT_TYPE = CommentsInput
    OUTPUT_TYPE = MultiClassificationOutput

    def _deploy(self, version: ModelVersion):
        # Deploy version
        logger.info(f"Deploying {version}")
        self.modelred = load_model("/bin/model.bin")

    def _predict(self, input_: InferenceInput) -> InferenceOutput:
        logger.info(input_)
        ... 
        
        # Report
        output = {
            'predictions': [
                {
                    'prediction': prediction_0,
                    'score': score_0,
                },
                {
                    'prediction': prediction_1,
                    'score': score_1,
                },
                {
                    'prediction': prediction_2,
                    'score': score_2,
                },
            ],
            'prediction': prediction_0,
            'score': score_0,
            'input': input_
        }
        logger.info(output)
        return self.OUTPUT_TYPE(**output)

    def _train(self, input_: List[InferenceOutput]):
        ...

if __name__ == '__main__':
    Classifier().serve_forever()
```

## Deployment recipe: docker-compose
Create a compose to deploy everything together
```
version: "3.2"
services:
  api:
    image: ml_api
    build:
      context: .
      dockerfile: ./api/Dockerfile
    ports:
      - "80:80"
    tty: true
    labels:
      - "traefik.enable=true"
      - "traefik.http.services.api.loadbalancer.server.port=80"
      - "traefik.http.routers.api.rule=Host(`api.localhost`)"
      - "traefik.http.routers.api.entrypoints=web"

  sentiment_analysis:
    image: sentiment_analysis
    build:
      context: ./
      dockerfile: ./sentiment_analysis/Dockerfile
    volumes:
      - ./sentiment_analysis/bin:/bin
    tty: true

  classifier:
    image: classifier
    build:
      context: ./
      dockerfile: ./classifier/Dockerfile
    volumes:
      - ./classifier/bin:/bin
    tty: true

  redis:
    image: redis:5.0.6
    ports:
      - 6379:6379

```

## How to run all:
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


## How to add your models?
1) Implement your own worker inheriting from `MLServiceInterface`
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

if __name__ == '__main__':
    MyNewModel().serve_forever()
```
2) add your model to the API
```python
...
from routers.my_new_model import MyNewModelAPI

MODELS_TO_DEPLOY = [
    ...
    MyNewModelAPI
]
```
3) Finally add your new service in the `docker-compose.yml` file
```yaml
  <MY_MODEL_NAME>:
    image: <MY_MODEL_NAME>
    build:
      context: ./
      dockerfile: ./<MY_MODEL_NAME>/Dockerfile
    tty: true
```
