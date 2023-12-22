from django.shortcuts import render, reverse
from django.contrib.auth.views import LoginView, LogoutView


def index(request):
    return render(
        request,
        "index.html",
    )


class UserLoginView(LoginView):
    template_name = "login.html"


class UserLogoutView(LogoutView):
    template_name = "logout.html"
