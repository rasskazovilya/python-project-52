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
    template_name = "users/user_list.html"
    model = User
    ordering = "id"
    paginate_by = 10
    context_object_name = "users"
    extra_context = {"title": gettext("Users")}


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = "obj_create.html"
    success_url = reverse_lazy("login")
    success_message = gettext("User created successfully")
    form_class = UserCreateForm
    extra_context = {
        "title": gettext("Create user"),
        "button_name": gettext("Sign up"),
    }


class UserUpdateView(
    LoginRequiredMsgMixin, SuccessMessageMixin, SameUserCheckMixin, UpdateView
):
    template_name = "obj_create.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("User edited successfully")
    form_class = UserCreateForm
    extra_context = {
        "title": gettext("Edit user"),
        "button_name": gettext("Edit"),
    }
    same_user_error_message = gettext(
        "You do not have rights to edit other user"
    )

    def get_same_user(self, pk):
        return self.model.objects.get(pk=pk)


class UserDeleteView(
    LoginRequiredMsgMixin, SuccessMessageMixin, SameUserCheckMixin, DeleteView
):
    template_name = "confirm_delete.html"
    model = User
    success_url = reverse_lazy("user_list")
    success_message = gettext("User deleted successfully")
    extra_context = {"title": gettext("Delete user")}
    same_user_error_message = gettext(
        "You do not have rights to delete other user"
    )

    def get_same_user(self, pk):
        return self.model.objects.get(pk=pk)

    def delete(self, *args, **kwargs):
        user = self.request.user
        creator_tasks = user.creator_tasks.filter(creator=user)
        performer_tasks = user.performer_tasks.filter(performer=user)

        if creator_tasks or performer_tasks:
            messages.error(
                self.request,
                gettext("Unable to delete user being in use"),
                extra_tags="danger",
            )
            return redirect(self.success_url)

        response = super().delete(*args, **kwargs)
        messages.success(self.request, self.success_message)
        return response
