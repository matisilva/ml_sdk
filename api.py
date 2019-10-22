from uuid import uuid4
import json
import time

from flask import Flask, request, jsonify, render_template
import redis

import settings


app = Flask(__name__)
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


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'text': None,
        'prediction': None,
        'score': None
    }

    text_data = request.form.get('text_data')
    print('LLego', text_data)
    if text_data:
        prediction, score = model_predict(text_data)
        context['text'] = text_data
        context['prediction'] = prediction
        context['score'] = round(100 * score, 2)

    return render_template('index.html', context=context)


@app.route('/predict', methods=['POST'])
def predict():
    # Initial response
    rpse = {
        'success': False,
        'prediction': None,
        'score': None
    }

    # Ensure method is correct and we have data to process
    if request.method == 'POST' and request.args.get('text'):
        # Get text from endpoint to analyze positiveness score
        text_data = request.args.get('text')
        app.logger.info('Received {}'.format(text_data))

        prediction, score = model_predict(text_data)
        rpse['prediction'] = prediction
        rpse['score'] = score

        # Successful request
        rpse['success'] = True

    return jsonify(rpse)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=settings.API_DEBUG)
