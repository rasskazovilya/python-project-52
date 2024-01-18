from django.db import models
from django.utils.translation import gettext

# Create your models here.
class Task(models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=gettext("Имя")
    )
    description = models.TextField(
        blank=True, verbose_name=gettext("Описание")
    )
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=gettext("Дата создания")
    )
    status = models.ForeignKey(
        "statuses.Status",
        on_delete=models.PROTECT,
        related_name="status",
        verbose_name=gettext("Статус"),
    )
    creator = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="creator",
        verbose_name=gettext("Создатель"),
    )
    performer = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="performer",
        verbose_name=gettext("Исполнитель"),
    )
