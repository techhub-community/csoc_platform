from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import Topic, Problem, Problem_Status
from .serializers import TopicSerializer, ProblemSerializer, ProblemStatusSerializer
from user.apis.permissions import CustomPermissionMixin


class TopicListCreateAPIView(CustomPermissionMixin, generics.ListCreateAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    authentication_classes = [JWTAuthentication]


class ProblemListCreateAPIView(CustomPermissionMixin, generics.ListCreateAPIView):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    authentication_classes = [JWTAuthentication]


class ProblemStatusListAPIView(generics.ListAPIView):
    queryset = Problem_Status.objects.all()
    serializer_class = ProblemStatusSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        query_set = super().get_queryset()
        return query_set.filter(user=self.request.user)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        result = Problem.objects.exclude(id__in=[item['question'] for item in response.data])
        result = ProblemSerializer(result, many=True).data
        result = [{'question': item['id'], 'status': 'PEN', 'user': request.user.id, 'id': None} for item in result]
        return Response(response.data + result)
