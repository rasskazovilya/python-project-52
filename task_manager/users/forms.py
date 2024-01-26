from task_manager.users.models import User

from django.contrib.auth.forms import UserCreationForm


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
        localized_fields = [
            "username",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
