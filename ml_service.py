import json
import time

from classifier import SentimentClassifier
import redis

import settings


# TODO
db = redis.StrictRedis(host=settings.REDIS_IP,
                       port=settings.REDIS_PORT,
                       db=settings.REDIS_DB_ID)

model = SentimentClassifier()


def sentiment_and_score(score):
    sentiment = None
    new_score = None
    if score < .45:
        sentiment = 'Negative'
        new_score = 1 - score
    elif score < .55:
        sentiment = 'Neutral'
        scaled_score = (score - .45) / (.55 - .45)
        new_score = 1 - scaled_score if scaled_score < .5 else scaled_score
    else:
        sentiment = 'Positive'
        new_score = score

    return sentiment, new_score


def classify_process():
    # TODO
    while True:
        # TODO
        queue = db.lrange(settings.REDIS_QUEUE,
                          settings.REDIS_DB_ID,
                          1)

        # TODO
        for q in queue:
            # TODO
            q = json.loads(q.decode("utf-8"))

            # TODO
            job_id = q["id"]

            # RUN ML MODEL...
            prediction = model.predict(q['text'])
            sentiment, score = sentiment_and_score(prediction)
            output = {
                'prediction': sentiment,
                'score': score
            }

            # TODO
            db.set(job_id, json.dumps(output))

            # TODO
            db.ltrim(settings.REDIS_QUEUE, 1, -1)

        # sleep for a small amount
        time.sleep(settings.SERVER_SLEEP)


if __name__ == "__main__":
    print('Loading ML model...')
    # Warm up model first
    model.predict('Warm up...')
    print('Model correctly loaded')

    # Now launch process
    print('Launching ML service...')
    classify_process()
