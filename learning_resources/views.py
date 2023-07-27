from rest_framework.generics import ListCreateAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from itertools import groupby

from .models import Resource
from .serializers import ResourceSerializer
from user.apis.permissions import CustomPermissionMixin


class ResourceListCreateAPIView(CustomPermissionMixin, ListCreateAPIView):
    serializer_class = ResourceSerializer
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return Resource.objects.all()

    def list(self, request, *args, **kwargs):
        resources = self.get_queryset()
        grouped_resources = {}
        resources = sorted(resources, key=lambda x: (x.domain, x.topic))
        for (domain, topic), group in groupby(resources, key=lambda x: (x.domain, x.topic)):
            if domain not in grouped_resources:
                grouped_resources[domain] = []
            topic_resources = [
                {"name": resource.name, "link": resource.link} for resource in group
            ]
            grouped_resources[domain].append(
                {"topic": topic, "resources": topic_resources})

        return Response(grouped_resources)
