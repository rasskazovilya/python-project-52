from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext


class LoginRequiredMsgMixin(LoginRequiredMixin):
    """
    A mixin that  displays an error message if a user is not authenticated
    and tries to access a view.
    """

    login_url = reverse_lazy("login")

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
                extra_tags="danger",
            )
            return redirect(self.login_url)
        return super().handle_no_permission()
