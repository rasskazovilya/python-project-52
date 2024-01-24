from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from task_manager.mixins import LoginRequiredMsgMixin

from .models import Label


# Create your views here.
class LabelListView(LoginRequiredMsgMixin, ListView):
    template_name = "label_list.html"
    model = Label
    ordering = "id"
    context_object_name = "labels"
    extra_context = {
        "title": gettext("Метки"),
        "button_name": gettext("Создать метку"),
    }


class LabelCreateView(LoginRequiredMsgMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("label_list")
    model = Label
    extra_context = {
        "title": gettext("Создать метку"),
        "button_name": gettext("Создать"),
    }
    fields = ["name"]


class LabelUpdateView(LoginRequiredMsgMixin, SuccessMessageMixin, UpdateView):
    template_name = "obj_create.html"
    model = Label
    success_url = reverse_lazy("label_list")
    success_message = gettext("Метка успешно изменена.")
    extra_context = {
        "title": gettext("Изменить метку"),
        "button_name": gettext("Изменить"),
    }
    fields = ["name"]


class LabelDeleteView(LoginRequiredMsgMixin, SuccessMessageMixin, DeleteView):
    template_name = "confirm_delete.html"
    success_url = reverse_lazy("label_list")
    success_message = gettext("Метка успешно удалена.")
    model = Label
    extra_context = {"title": gettext("Удалить метку")}

    def delete(self, *args, **kwargs):
        del_label = self.model.objects.get(pk=kwargs["pk"])

        if del_label.tasks.exists():
            messages.error(
                self.request,
                gettext(
                    "Невозможно удалить метку, потому что она используется"
                ),
                extra_tags="danger",
            )
            return redirect(self.success_url)
        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
