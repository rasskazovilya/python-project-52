from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic.base import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = "login.html"
    success_message = gettext("Successfully signed in. Greetings!")
    success_url = reverse_lazy("home")


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("home")

    def dispatch(self, request, *args, **kwargs):
        # if request.method == "GET":
        #     return HttpResponseNotAllowed("POST")
        # else:
        response = super().dispatch(request, *args, **kwargs)
        if not request.user.is_authenticated:
            messages.info(
                request, gettext("Successfully logged out. See you!")
            )
        return response
