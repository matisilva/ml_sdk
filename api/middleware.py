import json
import time
import redis
import settings
from uuid import uuid4
db = redis.StrictRedis(host=settings.REDIS_IP,
                       port=settings.REDIS_PORT,
                       db=settings.REDIS_DB_ID)


def model_predict(text_data):
    prediction = None
    score = None

    # Assign an unique ID for this job and add it to the queue
    job_id = str(uuid4())
    job_data = {
        'id': job_id,
        'text': text_data
    }

    db.rpush(settings.REDIS_QUEUE, json.dumps(job_data))

    # Loop until we received the response from our ML model
    while True:
        # Attempt to get model predictions by job_id
        output = db.get(job_id)

        # Check if the text was correctly processed by our ML model
        if output is not None:
            # Decode reponse from model and add it to our api response
            output = json.loads(output.decode("utf-8"))
            prediction = output['prediction']
            score = output['score']

            # Delete results from queue and exit loop
            db.delete(job_id)
            break

        # Sleep some time waiting for model results
        time.sleep(settings.API_SLEEP)

    return prediction, score
