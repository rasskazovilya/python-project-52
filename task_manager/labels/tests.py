from django.test import TestCase
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

    def test_add_label(self):
        response = self.client.post(
            reverse_lazy("create_label"), data=self.test_label, format="json"
        )
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        user = User.objects.first()
        self.client.force_login(user)
        response = self.client.post(
            reverse_lazy("create_label"), data=self.test_label, format="json"
        )
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("label_list"))

        new_item = Label.objects.last()
        self.assertEqual(new_item.name, self.test_label["name"])

    def test_edit_label(self):
        edit_url = reverse_lazy("edit_label", kwargs={"pk": 1})

        # check if unathorized user can not edit labels
        response = self.client.post(
            edit_url, data=self.test_label, format="json"
        )
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        # login user
        user = User.objects.first()
        self.client.force_login(user)

        # change label
        response = self.client.post(
            edit_url, data=self.test_label, format="json", follow=True
        )
        # check if redirect is correct and success message is showing
        self.assertEqual(200, response.status_code)
        self.assertRedirects(response, reverse_lazy("label_list"))
        self.assertContains(response, "Метка успешно изменена")

        # check if label has changed
        edited_label = Label.objects.get(id=1)
        self.assertEqual(edited_label.name, "Label1")

    def test_del_label(self):
        del_url = reverse_lazy("del_label", kwargs={"pk": 1})
        deleted_label = Label.objects.get(id=1)

        # check if unathorized user can not edit labels
        response = self.client.post(del_url)
        self.assertEqual(302, response.status_code)
        self.assertRedirects(response, reverse_lazy("login"))

        # login user
        user = User.objects.first()
        self.client.force_login(user)

        # try to delete label with related task
        response = self.client.post(del_url, follow=True)
        self.assertEqual(200, response.status_code)
        self.assertRedirects(response, reverse_lazy("label_list"))
        self.assertContains(
            response, "Невозможно удалить метку, потому что она используется"
        )

        # delete label from task
        Task.objects.filter(labels=deleted_label).first().labels.clear()
        # try again to delete label
        response = self.client.post(del_url, follow=True)
        # check if redirect is correct and success message is showing
        self.assertEqual(200, response.status_code)
        self.assertRedirects(response, reverse_lazy("label_list"))
        self.assertContains(response, "Метка успешно удалена")

        # check if label has been deleted
        self.assertNotIn(deleted_label, Label.objects.all())
