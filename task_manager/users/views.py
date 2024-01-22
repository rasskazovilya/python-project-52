from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.users.forms import UserCreateForm
from task_manager.users.models import User
from task_manager.mixins import LoginRequiredMsgMixin, SameUserCheckMixin
from django.core.exceptions import PermissionDenied


class UserListView(ListView):
    template_name = "user_list.html"
    model = User
    ordering = "id"
    paginate_by = 10
    context_object_name = "users"


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("login")
    success_message = gettext("Пользователь успешно зарегистрирован.")
    form_class = UserCreateForm
    extra_context = {
        "title": gettext("Создание пользователя"),
        "button_name": gettext("Создать"),
    }


class UserUpdateView(
    LoginRequiredMsgMixin, SuccessMessageMixin, SameUserCheckMixin, UpdateView
):
    template_name = "obj_create.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно изменен.")
    form_class = UserCreateForm
    extra_context = {
        "title": gettext("Изменение пользователя"),
        "button_name": gettext("Изменить"),
    }
    same_user_error_message = (
        "У вас нет прав для изменения другого пользователя."
    )

    def get_same_user(self, pk):
        return self.model.objects.get(pk=pk)


class UserDeleteView(
    LoginRequiredMsgMixin, SuccessMessageMixin, SameUserCheckMixin, DeleteView
):
    template_name = "confirm_delete.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно удален.")
    extra_context = {"title": gettext("Удаление пользователя")}
    same_user_error_message = (
        "У вас нет прав для удаления другого пользователя."
    )

    def get_same_user(self, pk):
        return self.model.objects.get(pk=pk)

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
