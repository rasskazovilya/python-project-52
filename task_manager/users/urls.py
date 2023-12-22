from django.urls import path

from task_manager.users import views

urlpatterns = [
    path("", views.UserListView.as_view(), name="user_list"),
    path("create/", views.UserCreateView.as_view(), name="signup"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="edit_user"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="del_user"),
]
