from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
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
    extra_context = {
        "title": "Statuses",
        "button_name": "Create status",
    }


class StatusCreateView(LoginRequiredMsgMixin, SuccessMessageMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext("Status created successfully")
    model = Status
    extra_context = {
        "title": "Create status",
        "button_name": "Create",
    }
    fields = ["name"]


class StatusUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext("Status edited successfully")
    model = Status
    extra_context = {
        "title": "Edit status",
        "button_name": "Edit",
    }
    fields = ["name"]


class StatusDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext("Status deleted successfully")
    model = Status
    extra_context = {"title": "Delete status"}

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
