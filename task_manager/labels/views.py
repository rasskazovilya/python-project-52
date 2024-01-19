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

from .models import Label


# Create your views here.
class LabelListView(LoginRequiredMsgMixin, ListView):
    template_name = "label_list.html"
    model = Label
    context_object_name = "labels"
    extra_context = {
        "title": gettext("Метки"),
        "button_name": gettext("Создать метку"),
    }


class LabelCreateView(LoginRequiredMsgMixin, CreateView):
    template_name = "label_create.html"
    success_url = reverse_lazy("label_list")
    model = Label
    extra_context = {"title": gettext("Создать метку")}
    fields = ["name"]


class LabelUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    pass


class LabelDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    pass
