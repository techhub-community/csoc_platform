from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Task, TaskStatus
from .serializers import TaskSerializer, ProgressSerializer
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

class ProgressAPIView(CustomPermissionMixin, generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = ProgressSerializer

    def get_object(self):
        user = self.request.user
        try:
            member = Member.objects.get(user=user.id, acceptance_status=True)
            team = member.team
        except Member.DoesNotExist:
            return {'progress': 0}

        total_tasks = Task.objects.filter(team=team).count()
        if total_tasks == 0:
            return {'progress': 0}

        verified_tasks = TaskStatus.objects.filter(member=member, status=TaskStatus.Choices.VERIFIED).count()
        progress = (verified_tasks / total_tasks) * 100
        return {'progress': progress}
