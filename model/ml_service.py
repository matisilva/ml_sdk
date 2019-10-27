import json
import time

from classifier import SentimentClassifier
import redis

import settings


# TODO
db = redis.Redis(host=settings.REDIS_IP,
                 port=settings.REDIS_PORT,
                 db=settings.REDIS_DB_ID)

model = SentimentClassifier()


def sentiment_from_score(score):
    sentiment = None

    if score < .45:
        sentiment = 'Negativo'
    elif score < .55:
        sentiment = 'Neutral'
    else:
        sentiment = 'Positivo'

    return sentiment


def predict(text):
    score = model.predict(text)
    score = round(score, 4)
    sentiment = sentiment_from_score(score)

    return sentiment, score


def classify_process():
    # TODO
    while True:
        # TODO
        queue = db.lrange(settings.REDIS_QUEUE, 0, 9)

        # TODO
        for q in queue:
            # TODO
            q = json.loads(q.decode("utf-8"))

            # TODO
            job_id = q["id"]

            # RUN ML MODEL...
            sentiment, score = predict(q['text'])
            output = {
                'prediction': sentiment,
                'score': score
            }

            db.set(job_id, json.dumps(output))

        db.ltrim(settings.REDIS_QUEUE, len(queue), -1)

        # sleep for a small amount
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print('Loading ML model...')
    # Warm up model first
    predict('Warm up...')
    print('Model correctly loaded')

    # Now launch process
    print('Launching ML service...')
    classify_process()
