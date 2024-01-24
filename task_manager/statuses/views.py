from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Status
from task_manager.mixins import LoginRequiredMsgMixin


# Create your views here.
class StatusListView(LoginRequiredMsgMixin, ListView):
    template_name = "statuses/status_list.html"
    model = Status
    ordering = "id"
    context_object_name = "statuses"
    extra_context = {"title": gettext("Статусы")}


class StatusCreateView(LoginRequiredMsgMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("status_list")
    model = Status
    extra_context = {
        "title": gettext("Создать статус"),
        "button_name": gettext("Создать"),
    }
    fields = ["name"]


class StatusUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext("Статус успешно изменен.")
    model = Status
    extra_context = {
        "title": gettext("Изменить статус"),
        "button_name": gettext("Изменить"),
    }
    fields = ["name"]


class StatusDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext("Статус успешно удален.")
    model = Status
    extra_context = {"title": gettext("Удалить статус")}

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
