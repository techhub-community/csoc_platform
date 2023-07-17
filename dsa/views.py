from rest_framework import generics, permissions
from rest_framework.response import Response

from .models import Topic, Problem, Status, Problem_Status
from .serializers import TopicSerializer, ProblemSerializer, StatusSerializer, ProblemStatusSerializer


class TopicListCreateAPIView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permission_classes(self):
        if self.request.method == 'POST':
            return [permissions.IsAdminUser]
        return super().get_permission_classes()

    

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ProblemStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem_Status.objects.all()
    serializer_class = ProblemStatusSerializer