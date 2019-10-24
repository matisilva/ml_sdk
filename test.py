import requests


def post_predict(text):
    url = 'http://0.0.0.0/predict'

    querystring = {'text': text}
    headers = {
        'cache-control': 'no-cache',
        'Postman-Token': '86a858d4-800e-404e-8dcd-24edd92936d7'
    }
    response = requests.request('POST', url, headers=headers,
                                params=querystring)

    return response


if __name__ == '__main__':
    text = 'La pelicula estuvo bien'
    rpse = post_predict(text)
    print('{}: {}'.format(text, rpse.json()))

    text = 'La pelicula estuvo excelente'
    rpse = post_predict(text)
    print('{}: {}'.format(text, rpse.json()))

    text = 'Me parecio una mala pelicula'
    rpse = post_predict(text)
    print('{}: {}'.format(text, rpse.json()))

    text = 'Fue una pelicula horrible'
    rpse = post_predict(text)
    print('{}: {}'.format(text, rpse.json()))

    text = 'Lalala lalal lal'
    rpse = post_predict(text)
    print('{}: {}'.format(text, rpse.json()))
