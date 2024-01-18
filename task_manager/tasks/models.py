from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.ForeignKey("statuses.Status", on_delete=models.PROTECT)
    creator = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="creator"
    )
    performer = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="performer"
    )
