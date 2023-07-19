from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task
from .serializers import TaskSerializer
from user.models import Member
from user.apis.permissions import CustomPermissionMixin


class TaskListCreateAPIView(CustomPermissionMixin, generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    
    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_superuser:
            return queryset
        try:
            team = Member.objects.get(user=user.id, acceptance_status=True).team
        except:
            return queryset.none()   
        return queryset.filter(team=team)


#Task Status cannot be created. It can only be updated. 
