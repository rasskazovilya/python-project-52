from django.urls import path

from task_manager.users import views

urlpatterns = [
    path("", views.UsersView.as_view()),
]
