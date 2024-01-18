from django.urls import path

from task_manager.tasks import views

urlpatterns = [
    path("", views.TaskListView.as_view(), name="task_list"),
    path("create/", views.TaskCreateView.as_view(), name="create_task"),
    path("<int:pk>/update/", views.TaskUpdateView.as_view(), name="edit_task"),
    path("<int:pk>/delete/", views.TaskDeleteView.as_view(), name="del_task"),
    path("<int:pk>/", views.TaskDetailView.as_view(), name="task_detail"),
]
