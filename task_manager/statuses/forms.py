from task_manager.statuses.models import Status
from django.utils.translation import gettext

from django.forms import ModelForm


class StatusCreateForm(ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        localized_fields = ["name"]
