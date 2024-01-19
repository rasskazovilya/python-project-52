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
    pass


class LabelUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    pass


class LabelDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    pass
