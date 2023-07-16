# from rest_framework import generics
# from .serializers import TopicSerializer
from rest_framework import generics
from rest_framework.response import Response
from .models import Topic, Problem, Status, Problem_Status
from .serializers import TopicSerializer, ProblemSerializer, StatusSerializer, ProblemStatusSerializer
from django.http import JsonResponse


# class TopicListCreateAPIView(generics.ListCreateAPIView):
#     queryset = Topic.obejcts.all()
#     serializer_class = TopicSerializer


class TopicListCreateAPIView(generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer

    def retrieve(self, request, *args, **kwargs):
        return Response({'something': 'my custom JSON'})

    def list(self, request, *args, **kwargs):
        return Response({'something': 'my custom JSON'})

    # def list(self, request, *args, **kwargs):
    #     topics = self.get_queryset()
    #     serializer = self.get_serializer(topics, many=True)
    #     return Response(serializer.data)

    

class ProblemListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

class StatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class ProblemStatusListCreateAPIView(generics.ListCreateAPIView):
    queryset = Problem_Status.objects.all()
    serializer_class = ProblemStatusSerializer