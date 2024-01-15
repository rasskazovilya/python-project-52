from django.urls import path

from task_manager.statuses import views

urlpatterns = [
    path("", views.StatusListView.as_view(), name="status_list"),
    path("create/", views.StatusCreateView.as_view(), name="create_status"),
    path(
        "<int:pk>/update/",
        views.StatusUpdateView.as_view(),
        name="edit_status",
    ),
    path(
        "<int:pk>/delete/", views.StatusDeleteView.as_view(), name="del_status"
    ),
]
