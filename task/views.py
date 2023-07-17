from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Task, TaskStatus, Badge
from .serializers import TaskSerializer, TaskStatusSerializer, BadgeSerializer

class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer

class BadgeListCreateAPIView(generics.ListCreateAPIView):
    queryset = Badge.objects.all()
    serializer_class = BadgeSerializer
