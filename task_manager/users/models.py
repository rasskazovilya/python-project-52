from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy


# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name=gettext_lazy("Username"),
        help_text=gettext_lazy(
            "Required. Less than 150 characters. Letters, numbers and @/./+/- only."
        ),
    )
    first_name = models.CharField(max_length=200, verbose_name=gettext_lazy("First Name"))
    last_name = models.CharField(max_length=200, verbose_name=gettext_lazy("Last Name"))
    password = models.CharField(max_length=200, verbose_name=gettext_lazy("Password"))
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.first_name + " " + self.last_name
