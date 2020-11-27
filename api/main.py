from typing import Optional

from fastapi import FastAPI, HTTPException
from ml_sdk.communication.kafka import KafkaDispatcher, KafkaSettings
from ml_sdk.model.input import TextInput

app = FastAPI()
kafka_settings = KafkaSettings(topic='sentiment_model', dns='kafka')
connector = KafkaDispatcher(kafka_settings)

app = FastAPI()


@app.post("/sentiment_model/predict")
def predict(input_: TextInput):
    return connector.dispatch('predict', input_=input_.dict())


@app.get("/sentiment_model/version")
def version():
    return connector.dispatch('version')


@app.get("/sentiment_model/train")
def train():
    raise HTTPException(status_code=404, detail="Not Implemented")


@app.get("/sentiment_model/test")
def test():
    raise HTTPException(status_code=404, detail="Not Implemented")


@app.get("/sentiment_model/deploy")
def deploy():
    raise HTTPException(status_code=404, detail="Not Implemented")

