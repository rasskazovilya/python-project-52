from django.urls import path

from task_manager.users import views

urlpatterns = [
    path("", views.UsersView.as_view()),
    path("create/", views.UserCreateView.as_view()),
    path("<int:id>/update/", views.UserUpdateView.as_view()),
    path("<int:id>/delete/", views.UserDeleteView.as_view()),
]
