from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    UpdateView,
    DetailView,
)
from task_manager.mixins import LoginRequiredMsgMixin

from .models import Task


# Create your views here.
class TaskListView(LoginRequiredMsgMixin, ListView):
    template_name = "task_list.html"
    model = Task
    context_object_name = "tasks"
    extra_context = {"title": gettext("Задачи")}


class TaskCreateView(LoginRequiredMsgMixin, CreateView):
    pass


class TaskUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    pass


class TaskDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    pass


class TaskDetailView(LoginRequiredMsgMixin, DetailView):
    pass
