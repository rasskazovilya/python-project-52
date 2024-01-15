from django.test import TestCase
from .models import Status
from django.urls import reverse_lazy

# Create your tests here.
class StatusTestCase(TestCase):
    fixtures = ["statuses.json"]

    def setUp(self):
        self.test_status = {
            "name": "Done",
        }

        self.test_statuses = []

        for i in range(5):
            status = {
                "name": f"Test_{i}",
            }
            self.test_statuses.append(status)
        return super().setUp()

    def test_status_list(self):
        response = self.client.get(reverse_lazy("status_list"))

        for status in self.test_statuses:
            self.assertContains(response, status["name"])
