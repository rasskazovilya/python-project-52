from django.test import TestCase
from .models import Status
from task_manager.users.models import User
from django.urls import reverse_lazy

# Create your tests here.
class StatusTestCase(TestCase):
    fixtures = ["statuses.json"]

    def setUp(self):
        self.test_user = {
            "username": "Test",
            "first_name": "Test",
            "last_name": "Test",
            "password": "Test",
        }
        User.objects.create(**self.test_user)

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
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.get(reverse_lazy("status_list"))
        for status in self.test_statuses:
            self.assertContains(response, status["name"])

    def test_add_status(self):
        # check if unathorized user can not create statuses
        response = self.client.post(
            reverse_lazy("create_status"), data=self.test_status, format="json"
        )
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        # login user
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.post(
            reverse_lazy("create_status"), data=self.test_status, format="json"
        )
        # check that logged user is redirected to status list page
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("status_list"))

        # check if new status is added
        new_item = Status.objects.last()
        self.assertEqual(new_item.name, self.test_status["name"])
