from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Status


# Create your views here.
class StatusListView(ListView):
    template_name = "status_list.html"
    model = Status
    context_object_name = "statuses"


class StatusCreateView(CreateView):
    pass


class StatusUpdateView(UpdateView):
    pass


class StatusDeleteView(DeleteView):
    pass
