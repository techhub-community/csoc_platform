from rest_framework import generics
from rest_framework.response import Response

from .models import Topic, Problem, Status, Problem_Status
from .serializers import TopicSerializer, ProblemSerializer, StatusSerializer, ProblemStatusSerializer


class TopicListCreateAPIView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    # def list(self, request, *args, **kwargs):
    #     return Response(status=200, 
    #                     data=[{'something': 'utkarsh my custom JSON',},],)

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ProblemStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem_Status.objects.all()
    serializer_class = ProblemStatusSerializer