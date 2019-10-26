import unittest
import json
import os.path
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir))
from app import app


class TestAPI(unittest.TestCase):
    POS_SENT = 'Esta es una oracion positiva y estoy contento por eso'
    NEG_SENT = 'Tenemos problemas de inseguridad'

    def test_bad_parameters(self):
        response = app.test_client().post(
            '/predict',
            data=json.dumps({'text': self.POS_SENT}),
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['success'], False)

    def test_ok_positive(self):
        response = app.test_client().post(
            '/predict',
            query_string={'text': self.POS_SENT},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['success'], True)

    def test_ok_negative(self):
        response = app.test_client().post(
            '/predict',
            query_string={'text': self.NEG_SENT},
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['success'], True)

    def test_template_endpoint(self):
        response = app.test_client().get('/')
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
