from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
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
