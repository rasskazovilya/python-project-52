from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext


def index(request):
    return render(
        request,
        "index.html",
    )


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = gettext(
        "Successfully signed in. Greetings, %(username)s!"
    )
    success_url = reverse_lazy("home")


class UserLogoutView(LogoutView):
    template_name = "logout.html"
