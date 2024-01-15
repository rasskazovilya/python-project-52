from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

# Create your views here.
class StatusListView(ListView):
    pass


class StatusCreateView(CreateView):
    pass


class StatusUpdateView(UpdateView):
    pass


class StatusDeleteView(DeleteView):
    pass
