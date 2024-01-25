import django_filters
from task_manager.labels.models import Label
from task_manager.tasks.models import Task
from django.utils.translation import gettext
from django import forms


class TaskFilter(django_filters.FilterSet):
    class Meta:
        model = Task
        fields = ["status", "performer"]

    labels = django_filters.ModelChoiceFilter(
        label=gettext("Label"), queryset=Label.objects.all()
    )
    creator = django_filters.BooleanFilter(
        method="filter_creator_tasks",
        widget=forms.CheckboxInput,
        label=gettext("Only own tasks"),
    )

    def filter_creator_tasks(self, queryset, name, value):
        if value:
            lookup = name + "__exact"
            return queryset.filter(**{lookup: self.request.user})
        return queryset
