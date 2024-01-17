from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.users.forms import UserCreateForm
from task_manager.users.models import User


class UserListView(ListView):
    template_name = "user_list.html"
    model = User
    ordering = "id"
    paginate_by = 10
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "user_create.html"
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно зарегистрирован.")
    form_class = UserCreateForm
    extra_context = {"title": gettext("Создание пользователя")}


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = "user_create.html"
    login_url = reverse_lazy("login")
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно изменен.")
    form_class = UserCreateForm
    extra_context = {"title": gettext("Изменение пользователя")}

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
                extra_tags="danger",
            )
            return redirect(self.login_url)
        same_user = self.model.objects.get(pk=kwargs["pk"])
        if self.request.user != same_user:
            messages.error(
                self.request,
                gettext("У вас нет прав для изменения другого пользователя."),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        return super().dispatch(*args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    login_url = reverse_lazy("login")
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно удален.")
    extra_context = {"title": gettext("Удаление пользователя")}

    def dispatch(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
                extra_tags="danger",
            )
            return redirect(self.login_url)
        same_user = self.model.objects.get(pk=kwargs["pk"])
        if self.request.user != same_user:
            messages.error(
                self.request,
                gettext("У вас нет прав для удаления другого пользователя."),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        return super().dispatch(*args, **kwargs)

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
