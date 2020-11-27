from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ml_sdk.communication.kafka import KafkaRPCDispatcher, KafkaSettings

app = FastAPI()
kafka_settings = KafkaSettings(topic='sentiment_model', dns='kafka')
dispatcher = KafkaRPCDispatcher(kafka_settings)


class TextInput(BaseModel):
    text: str

app = FastAPI()


@app.post("/sentiment_model/predict")
def predict(input_: TextInput):
    return dispatcher.dispatch('predict', input_=input_.text)


@app.get("/sentiment_model/version")
def version():
    return dispatcher.dispatch('version')


@app.get("/sentiment_model/train")
def train():
    raise HTTPException(status_code=404, detail="Not Implemented")


@app.get("/sentiment_model/test")
def test():
    raise HTTPException(status_code=404, detail="Not Implemented")


@app.get("/sentiment_model/deploy")
def deploy():
    raise HTTPException(status_code=404, detail="Not Implemented")

