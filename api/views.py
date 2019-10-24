import settings

from flask import Flask, request, jsonify, render_template
from middleware import model_predict

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'text': None,
        'prediction': None,
        'score': None
    }

    text_data = request.form.get('text_data')

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

        prediction, score = model_predict(text_data)
        rpse['prediction'] = prediction
        rpse['score'] = score

        # Successful request
        rpse['success'] = True

    return jsonify(rpse)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=settings.API_DEBUG)
