from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.shortcuts import redirect

from .models import Status
from task_manager.mixins import LoginRequiredMsgMixin


# Create your views here.
class StatusListView(LoginRequiredMsgMixin, ListView):
    template_name = "statuses/status_list.html"
    model = Status
    ordering = "id"
    context_object_name = "statuses"
    extra_context = {
        "title": gettext_lazy("Statuses"),
        "button_name": gettext_lazy("Create status"),
    }


class StatusCreateView(LoginRequiredMsgMixin, SuccessMessageMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext_lazy("Status created successfully")
    model = Status
    extra_context = {
        "title": gettext_lazy("Create status"),
        "button_name": gettext_lazy("Create"),
    }
    fields = ["name"]


class StatusUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext_lazy("Status edited successfully")
    model = Status
    extra_context = {
        "title": gettext_lazy("Edit status"),
        "button_name": gettext_lazy("Edit"),
    }
    fields = ["name"]


class StatusDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("status_list")
    success_message = gettext_lazy("Status deleted successfully")
    model = Status
    extra_context = {"title": gettext_lazy("Delete status")}

    def delete(self, *args, **kwargs):
        del_status = self.model.objects.get(pk=kwargs["pk"])

        if del_status.tasks.exists():
            messages.error(
                self.request,
                gettext_lazy("Unable to delete status as it is being in use"),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
