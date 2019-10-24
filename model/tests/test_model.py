import unittest
import os.path
import sys
sys.path.append(os.path.join(
    os.path.dirname(os.path.realpath(__file__)), os.pardir))
from ml_service import predict


class TestMLService(unittest.TestCase):

    # def setUp(self):
    #     self.model = model
    #     self.db = db

    def test_model_response(self):
        pos_sentence = 'Me gusto la pelicula'
        pos_score = 0.975
        pos_prediction = predict(pos_sentence)
        self.assertAlmostEqual(pos_prediction, pos_score, places=3)

        neg_sentence = 'No me gusto la pelicula'
        neg_score = 0.358
        neg_prediction = predict(neg_sentence)
        self.assertAlmostEqual(neg_prediction, neg_score, places=3)

    def test_db_conn(self):
        # TODO
        # db.ping()
        pass


if __name__ == '__main__':
    unittest.main()
