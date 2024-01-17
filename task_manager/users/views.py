from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.users.forms import UserCreateForm
from task_manager.users.models import User
from task_manager.mixins import LoginRequiredMsgMixin


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


class UserUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    template_name = "user_create.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно изменен.")
    form_class = UserCreateForm
    extra_context = {"title": gettext("Изменение пользователя")}

    def get(self, request, *args, **kwargs):
        same_user = self.model.objects.get(pk=kwargs["pk"])
        if request.user != same_user:
            messages.error(
                self.request,
                gettext("У вас нет прав для изменения другого пользователя."),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("Пользователь успешно удален.")
    extra_context = {"title": gettext("Удаление пользователя")}

    def get(self, request, *args, **kwargs):
        same_user = self.model.objects.get(pk=kwargs["pk"])
        if request.user != same_user:
            messages.error(
                self.request,
                gettext("У вас нет прав для удаления другого пользователя."),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        return super().get(request, *args, **kwargs)

    def delete(self, *args, **kwargs):
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
