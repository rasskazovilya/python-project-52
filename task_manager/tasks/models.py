from django.db import models
from django.utils.translation import gettext_lazy


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name=gettext_lazy("Task Name"))
    description = models.TextField(blank=True, verbose_name=gettext_lazy("Description"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=gettext_lazy("Created at"))
    status = models.ForeignKey(
        "statuses.Status",
        on_delete=models.PROTECT,
        related_name="tasks",
        verbose_name=gettext_lazy("Status"),
    )
    creator = models.ForeignKey(
        "users.User",
        on_delete=models.PROTECT,
        related_name="creator_tasks",
        verbose_name=gettext_lazy("Creator"),
    )
    executor = models.ForeignKey(
        "users.User",
        blank=True,
        null=True,
        on_delete=models.PROTECT,
        related_name="performer_tasks",
        verbose_name=gettext_lazy("Performer"),
    )
    labels = models.ManyToManyField(
        "labels.Label",
        blank=True,
        through="TaskLabelRelation",
        verbose_name=gettext_lazy("Labels"),
        related_name="tasks",
    )

    def __str__(self):
        return self.name


class TaskLabelRelation(models.Model):
    """
    Additional model for ManyToMany field in the Tasks model.
    It's needed because Django doesn't allow to set on delete=models.PROTE
    """

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name="label_tasks",
        blank=True,
    )
    label = models.ForeignKey(
        "labels.Label",
        on_delete=models.PROTECT,
        related_name="task_labels",
        blank=False,
    )
