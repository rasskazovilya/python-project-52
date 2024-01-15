from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .models import Status


# Create your views here.
class StatusListView(LoginRequiredMixin, ListView):
    template_name = "status_list.html"
    login_url = reverse_lazy("login")
    model = Status
    context_object_name = "statuses"
    extra_context = {"title": gettext("Статусы")}

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
                extra_tags="danger",
            )
            return redirect(self.login_url)
        return super().handle_no_permission()


class StatusCreateView(LoginRequiredMixin, CreateView):
    template_name = "status_create.html"
    login_url = reverse_lazy("login")
    success_url = reverse_lazy("status_list")
    model = Status
    extra_context = {"title": gettext("Создать статус")}
    fields = ["name"]

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                gettext("Вы не авторизованы! Пожалуйста, выполните вход."),
                extra_tags="danger",
            )
            return redirect(self.login_url)
        return super().handle_no_permission()


class StatusUpdateView(UpdateView):
    pass


class StatusDeleteView(DeleteView):
    pass
