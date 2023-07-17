from django.urls import path

from .views import TaskListCreateAPIView, TaskStatusListCreateAPIView, BadgeListCreateAPIView

app_name = 'dsa'


urlpatterns = [
    path('task/', TaskListCreateAPIView.as_view(), name='topic-list-create'),
    path('task-status/', TaskStatusListCreateAPIView.as_view(), name='problem-list-create'),
    path('badge/', BadgeListCreateAPIView.as_view(), name='status-list-create'),
]
