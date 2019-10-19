import requests


if __name__ == '__main__':
    url = 'http://0.0.0.0:5000/predict'

    querystring = {'text': 'lalalalla'}
    headers = {
        'cache-control': 'no-cache',
        'Postman-Token': '86a858d4-800e-404e-8dcd-24edd92936d7'
    }
    response = requests.request('POST', url, headers=headers,
                                params=querystring)
    print(response.text)
