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

    def test_add_task(self):
        # check if unathorized user can not create tasks
        response = self.client.post(
            reverse_lazy("create_task"), data=self.test_task, format="json"
        )
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        # login user
        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.post(
            reverse_lazy("create_task"), data=self.test_task, format="json"
        )
        # check that logged user is redirected to task list page
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("task_list"))

        # check if new status is added
        new_item = Task.objects.last()
        self.assertEqual(new_item.name, self.test_task["name"])
        self.assertEqual(new_item.creator, User.objects.get(id=1))

