from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.views import View

from task_manager.users.models import User


class UsersView(View):
    template_name = "users.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
