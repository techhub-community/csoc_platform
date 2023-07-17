from django.urls import path

from .views import TaskListCreateAPIView, TaskStatusListCreateAPIView

app_name = 'dsa'


urlpatterns = [
    path('<int:pk>/', TaskListCreateAPIView.as_view(), name='topic-list-create'),
    path('status/', TaskStatusListCreateAPIView.as_view(), name='problem-list-create'),
]
