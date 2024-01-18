from django.test import TestCase
from task_manager.statuses.models import Status
from task_manager.users.models import User
from task_manager.tasks.models import Task
from django.urls import reverse_lazy

# Create your tests here.
class TaskTestCase(TestCase):
    fixtures = ["tasks.json"]

    def setUp(self):
        self.test_user = {
            "username": "Test",
            "first_name": "Test",
            "last_name": "Test",
            "password": "Test",
        }
        User.objects.create(**self.test_user)

        # self.test_status = {
        #     "name": "Done",
        # }
        # Status.objects.create(**self.test_status)

        self.test_task = {
            "name": "Task1",
            "description": "Desc1",
            "status": 1,
            "creator": 1,
            "performer": 1,
        }

        return super().setUp()

    def test_task_list(self):
        response = self.client.get(reverse_lazy("task_list"))
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        task = Task.objects.first()
        user = User.objects.first()
        self.client.force_login(user)

        response = self.client.get(reverse_lazy("task_list"))
        self.assertEqual(200, response.status_code)
        self.assertContains(response, task.name)

