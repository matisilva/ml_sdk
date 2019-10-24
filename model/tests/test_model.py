import unittest

import ml_service


class TestMLService(unittest.TestCase):

    # def setUp(self):
    #     self.model = model
    #     self.db = db

    def test_model_response(self):
        pos_sentence = 'Me gusto la pelicula'
        pos_score = 0.975
        pos_prediction = ml_service.predict(pos_sentence)
        print(pos_prediction)
        self.assertAlmostEqual(pos_prediction, pos_score, places=3)

        neg_sentence = 'No me gusto la pelicula'
        neg_score = 0.358
        neg_prediction = ml_service.predict(neg_sentence)
        print(neg_prediction)
        self.assertAlmostEqual(neg_prediction, neg_score, places=3)

    def test_db_conn(self):
        # TODO
        #ml_service.db.ping()


if __name__ == '__main__':
    unittest.main()
