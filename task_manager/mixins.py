from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic.detail import SingleObjectMixin
from task_manager.users.models import User


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
        return False


class SameUserCheckMixin(SingleObjectMixin):
    model = User
    same_user_error_message = gettext(
        "У вас нет прав для изменения/удаления другого пользователя."
    )
    success_url = ""

    def dispatch(self, *args, **kwargs):
        if self.handle_no_permission():
            return redirect(self.login_url)
        same_user = self.get_same_user(pk=kwargs["pk"])
        if self.request.user != same_user:
            messages.error(
                self.request,
                self.same_user_error_message,
                extra_tags="danger",
            )
            return redirect(self.success_url)
        return super().dispatch(*args, **kwargs)

    def get_same_user(self):
        # This method should be overridden in the child classes of this MixIn
        raise NotImplementedError()
