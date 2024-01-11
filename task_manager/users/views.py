from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.users.forms import UserCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.utils.translation import gettext


class UserListView(ListView):
    template_name = "user_list.html"
    model = User
    paginate_by = 10
    context_object_name = "users"


class UserCreateView(CreateView):
    template_name = "user_create.html"
    success_url = reverse_lazy("user_list")
    form_class = UserCreateForm


class UserUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "user_create.html"
    login_url = reverse_lazy("login")
    model = User
    success_url = reverse_lazy("user_list")
    form_class = UserCreateForm

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


class UserDeleteView(LoginRequiredMixin, DeleteView):
    template_name = "confirm_delete.html"
    login_url = reverse_lazy("login")
    model = User
    success_url = reverse_lazy("user_list")

    def dispatch(self, request, *args, **kwargs):
        messages.error(
            request,
            gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
            extra_tags="danger",
        )
        return super().dispatch(request, *args, **kwargs)
