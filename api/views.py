from flask import (
    Blueprint,
    request,
    jsonify,
    render_template,
)
from middleware import model_predict


router = Blueprint('app_name',
                   __name__,
                   template_folder='templates')


@router.route('/', methods=['GET', 'POST'])
def index():
    context = {
        'text': None,
        'prediction': None,
        'score': None,
        'success': False
    }

    text_data = request.form.get('text_data')

    if text_data:
        prediction, score = model_predict(text_data)
        context['text'] = text_data
        context['prediction'] = prediction
        context['success'] = True
        context['score'] = round(100 * score, 2)
    return render_template('index.html', context=context)


@router.route('/feedback', methods=['GET', 'POST'])
def feedback():
    report = request.form.get('report')
    if report:
        with open("feedback", "a+") as f:
            f.write(report + "\n")
    return render_template('index.html', context={})


@router.route('/predict', methods=['POST'])
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
    return jsonify(rpse), 400
