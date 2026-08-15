
import locust

class WebsiteUser(locust.HttpUser):
    host = "http://localhost:8000"
    wait_time = locust.between(1, 2)

    @locust.task
    def index_page(self):
        self.client.get("/")

    @locust.task
    def predict_endpoint(self):
        self.client.post("/predict", json={"text": "This is a test sentence for sentiment analysis."})
