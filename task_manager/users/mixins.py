from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.utils.translation import gettext
from django.urls import reverse_lazy
from django.shortcuts import redirect

# TODO: change update and delete views in users/views.py
# to subclass UserAccessMixin
class UserAccessMixin(AccessMixin):
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("user_list")

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(
                self.request,
                gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
                extra_tags="danger",
            )
            return redirect(self.login_url)
        same_user = self.model.objects.get(pk=kwargs["pk"])
        if request.user != same_user:
            messages.error(
                self.request,
                gettext("У вас нет прав для изменения другого пользователя."),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    # def get_object(self, queryset=None):
    #     obj = super().get_object(queryset=queryset)
    #     if self.request.user != obj:
    #         messages.error(
    #             self.request,
    #             gettext("У вас нет прав для изменения другого пользователя."),
    #             extra_tags="danger",
    #         )
    #         return redirect(self.success_url)
    #     return obj
