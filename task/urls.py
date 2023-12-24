from django.urls import path

from .views import TaskListCreateAPIView, ProgressAPIView

app_name = 'task'

urlpatterns = [
    path('', TaskListCreateAPIView.as_view(), name='topic-list-create'),
    path('progress/', ProgressAPIView.as_view(), name='task_progress'),
]
