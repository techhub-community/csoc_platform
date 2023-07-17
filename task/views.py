from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Task, TaskStatus
from .serializers import TaskSerializer, TaskStatusSerializer

#1. Separate the list and createVIew for task 
#2. The List View should only send the list of tasks that are associated with the particular team those pk which has been passed in the URL
#3. 
class TaskListCreateAPIView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

#Use ListAPIView/RetrieveAPIView to fetch the data for a task associated with a particular user
#Task Status cannot be created. It can only be updated. 
class TaskStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = TaskStatus.objects.all()
    serializer_class = TaskStatusSerializer