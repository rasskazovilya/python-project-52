from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView
from django_filters.views import FilterView
from task_manager.mixins import LoginRequiredMsgMixin, SameUserCheckMixin
from task_manager.tasks.filter import TaskFilter

from .models import Task


# Create your views here.
class TaskListView(LoginRequiredMsgMixin, FilterView):
    template_name = "tasks/task_list.html"
    model = Task
    ordering = "id"
    filterset_class = TaskFilter
    context_object_name = "tasks"
    extra_context = {"title": "Tasks", "button_name": "Create task"}


class TaskCreateView(LoginRequiredMsgMixin, SuccessMessageMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("task_list")
    success_message = gettext("Task created successfully")
    model = Task
    extra_context = {
        "title": "Create task",
        "button_name": "Create",
    }
    fields = ["name", "description", "status", "executor", "labels"]

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("task_list")
    success_message = gettext("Task edited successfully")
    model = Task
    extra_context = {
        "title": "Edit task",
        "button_name": "Edit",
    }
    fields = ["name", "description", "status", "executor", "labels"]


class TaskDeleteView(LoginRequiredMsgMixin, SameUserCheckMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("task_list")
    success_message = gettext("Task deleted successfully")
    model = Task
    extra_context = {"title": "Delete task"}
    same_user_error_message = gettext("Task can be deleted only by its author")

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response

    def get_same_user(self, pk):
        task = Task.objects.get(pk=pk)
        return task.creator


class TaskDetailView(LoginRequiredMsgMixin, DetailView):
    template_name = "tasks/task_detail.html"
    context_object_name = "task"
    model = Task
    extra_context = {"title": "Task detail"}
