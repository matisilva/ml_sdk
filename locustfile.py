from locust import HttpUser, task


class UserBehavior(HttpUser):

    @task(1)
    def index(self):
        self.client.get('/sentiment_model/version')

    @task(2)
    def index(self):
        self.client.post('/sentiment_model/predict', json={'text': 'dolar'})