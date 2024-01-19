from django.test import TestCase
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.tasks.models import Task
from task_manager.labels.models import Label
from django.urls import reverse_lazy

# Create your tests here.
class LabelTestCase(TestCase):
    fixtures = ["labels.json"]

    def setUp(self):
        self.test_user = {
            "username": "Test",
            "first_name": "Test",
            "last_name": "Test",
            "password": "Test",
        }
        User.objects.create(**self.test_user)

        self.test_label = {
            "name": "Label1",
        }

        return super().setUp()

    def test_label_list(self):
        response = self.client.get(reverse_lazy("label_list"))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        label = Label.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

        response = self.client.get(reverse_lazy("label_list"))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, label.name)
