from uuid import uuid4
import json
import time

from flask import Flask, request, jsonify
import redis

import settings


app = Flask(__name__)
db = redis.StrictRedis(host=settings.REDIS_IP,
                       port=settings.REDIS_PORT,
                       db=settings.REDIS_DB_ID)


@app.route('/')
def index():
    return 'Index Page'


@app.route('/predict', methods=['POST'])
def predict():
    # Initial response
    rpse = {
        'success': False,
        'prediction': ''
    }

    # Ensure method is correct and we have data to process
    if request.method == 'POST' and request.args.get('text'):
        # Get text from endpoint to analyze positiveness score
        text_data = request.args.get('text')
        app.logger.info('Received {}'.format(text_data))

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
                output = output.decode("utf-8")
                rpse['prediction'] = json.loads(output)

                # Delete results from queue and exit loop
                db.delete(job_id)
                break

            # Sleep some time waiting for model results
            time.sleep(settings.API_SLEEP)

        # Successful request
        rpse['success'] = True

    return jsonify(rpse)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=settings.API_DEBUG)
