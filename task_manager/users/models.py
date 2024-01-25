from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext

# Create your models here.
class User(AbstractUser):
    username = models.CharField(
        max_length=150, unique=True, verbose_name=gettext("Username")
    )
    first_name = models.CharField(
        max_length=200, verbose_name=gettext("First Name")
    )
    last_name = models.CharField(
        max_length=200, verbose_name=gettext("Last Name")
    )
    password = models.CharField(
        max_length=200, verbose_name=gettext("Password")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = "username"
