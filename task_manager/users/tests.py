from django.test import TestCase
from task_manager.users.models import User
from django.urls import reverse_lazy

# TODO: Test translation using this link: https://docs.djangoproject.com/en/5.0/topics/testing/tools/#setting-the-language

# Create your tests here.
class UserListTestCase(TestCase):
    fixtures = ["users.json"]

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

    def test_user_list(self):
        response = self.client.get(
            reverse_lazy("user_list"),
        )

        content = response.content.decode()

        for user in self.test_users:
            self.assertIn(user["username"], content)

    def test_add_user(self):
        response = self.client.post(
            reverse_lazy("signup"), data=self.test_user, format="json"
        )

        self.assertEqual(response.status_code, 302, "Status code is not 302")

        new_user = User.objects.last()
        self.assertIsInstance(new_user, User)
        self.assertEqual(new_user.username, "JohnDoe")
        self.assertEqual(new_user.pk, 6)
        self.assertTrue(new_user.check_password("secure_password"))

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
