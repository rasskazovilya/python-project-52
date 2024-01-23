from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse_lazy

# TODO: Test translation using this link: https://docs.djangoproject.com/en/5.0/topics/testing/tools/#setting-the-language

# Create your tests here.
class UserListTestCase(TestCase):
    fixtures = ["users.json"]
    login_url = reverse_lazy("login")

    def setUp(self):
        self.test_user = {
            "username": "JohnDoe",
            "first_name": "John",
            "last_name": "Doe",
            "password1": "secure_password",
        }
        self.test_user.update({"password2": self.test_user["password1"]})

        # the same list as in "users.json" fixture
        self.test_users = []

        for i in range(5):
            user = {
                "username": f"Test_{i}",
                "first_name": f"Test_first_name_{i}",
                "last_name": f"Test_last_name_{i}",
                "password1": f"pass{i}",
                "password2": f"pass{i}",
            }
            self.test_users.append(user)
        return super().setUp()

    def test_user_list(self):
        response = self.client.get(
            reverse_lazy("user_list"),
        )

        content = response.content.decode()

        for user in self.test_users:
            self.assertIn(user["username"], content)

    def test_add_user(self):
        response = self.client.post(
            reverse_lazy("signup"),
            data=self.test_user,
            format="json",
            follow=True,
        )

        self.assertEqual(response.status_code, 200)

        new_user = User.objects.last()
        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, "JohnDoe")
        self.assertEqual(new_user.pk, 6)
        self.assertTrue(new_user.check_password("secure_password"))
        self.assertContains(response, "Пользователь успешно зарегистрирован.")

    def test_password_not_confirmed(self):
        test_user_wrong_password = self.test_user.copy()
        test_user_wrong_password.update({"password2": "other_password"})

        response = self.client.post(
            reverse_lazy("signup"),
            data=test_user_wrong_password,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            200,
            "Status code should be 200 for not confirmed password",
        )
        page = response.content.decode()
        self.assertIn("The two password fields didn’t match.", str(page))

    def test_edit_user(self):
        edit_url = reverse_lazy("edit_user", kwargs={"pk": 1})
        other_edit_url = reverse_lazy("edit_user", kwargs={"pk": 4})
        # no logged user
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # try to login with user not in db
        self.client.login(
            username=self.test_user["username"],
            password=self.test_user["password1"],
        )
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # login with user in db
        first_user = User.objects.first()
        self.client.force_login(first_user)

        ## try to get edit page for another user
        response = self.client.get(other_edit_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("user_list"))
        ## check if error message about not authorized user is in place
        response = self.client.get(other_edit_url, follow=True)
        self.assertContains(
            response,
            "У вас нет прав для изменения другого пользователя.",
        )

        ## get edit page for current user
        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)

        ## edit current user
        data = {
            "username": f"New Test_1",
            "first_name": f"New Test_first_name_1",
            "last_name": f"New Test_last_name_1",
            "password1": f"new_pass1",
            "password2": f"new_pass1",
        }

        response = self.client.post(other_edit_url, data=data, follow=True)
        self.assertContains(
            response,
            "У вас нет прав для изменения другого пользователя.",
        )

        response = self.client.post(edit_url, data=data, follow=True)
        self.assertTrue(User.objects.filter(username="New Test_1").exists())
        self.assertRedirects(response, reverse_lazy("user_list"))
        self.assertContains(response, "Пользователь успешно изменен.")

    def test_delete_user(self):
        delete_url = reverse_lazy("del_user", kwargs={"pk": 1})
        other_delete_url = reverse_lazy("del_user", kwargs={"pk": 2})
        # no logged user
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # try to login with user not in db
        self.client.login(
            username=self.test_user["username"],
            password=self.test_user["password1"],
        )
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.login_url)

        # login with user in db
        first_user = User.objects.first()
        self.client.force_login(first_user)

        ## try to get edit page for another user
        response = self.client.get(other_delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse_lazy("user_list"))
        ## check if error message about not authorized user is in place
        response = self.client.get(other_delete_url, follow=True)
        self.assertContains(
            response,
            "У вас нет прав для удаления другого пользователя.",
        )

        ## make sure that you can not delete user with created tasks
        second_user = User.objects.get(id=2)
        self.client.force_login(second_user)
        print(second_user.creator_tasks.filter(creator=second_user).all())
        print(second_user.creator_tasks.filter(creator=second_user).exists())
        response = self.client.post(other_delete_url, follow=True)
        self.assertRedirects(response, reverse_lazy("user_list"))
        self.assertTrue(User.objects.filter(id=2).exists())
        self.assertContains(
            response,
            "Невозможно удалить пользователя, потому что он используется",
        )

        ## get delete page for current user
        self.client.force_login(first_user)
        response = self.client.get(delete_url)
        self.assertEqual(response.status_code, 200)

        ## delete current user
        print(first_user.creator_tasks.filter(creator=first_user).all())
        response = self.client.post(delete_url, follow=True)
        self.assertFalse(User.objects.filter(id=1).exists())
        self.assertRedirects(response, reverse_lazy("user_list"))
        self.assertContains(response, "Пользователь успешно удален.")
