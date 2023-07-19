from django.urls import path

from .views import TaskListCreateAPIView

app_name = 'task'

urlpatterns = [
    path('', TaskListCreateAPIView.as_view(), name='topic-list-create')
]
