from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext


class IndexView(TemplateView):
    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = gettext("Successfully signed in. Greetings!")
    success_url = reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, gettext("Successfully logged out. See you!"))
        return super().dispatch(request, *args, **kwargs)
