from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from collections import defaultdict

from .models import Resource
from .serializers import ResourceSerializer
from user.apis.permissions import CustomPermissionMixin


class ResourceListAPIView(CustomPermissionMixin, ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    authentication_classes = [JWTAuthentication]


    def get_resource_data(self, resource_data):
        return {
            "description": resource_data['description'],
            "link": resource_data['link'],
        }

    def generate_grouped_resources(self):
        resources = Resource.objects.values('program__name', 'topic', 'description', 'link')
        grouped_resources = defaultdict(lambda: defaultdict(list))
        [
            grouped_resources[resource_data['program__name']][resource_data['topic']].append(self.get_resource_data(resource_data))
            for resource_data in resources
        ]
        return grouped_resources

    def get(self, request, *args, **kwargs):
        grouped_resources = self.generate_grouped_resources()
        response_data = {
            program_name: [{"topic": topic, "resources": resources_list} for topic, resources_list in topics.items()]
            for program_name, topics in grouped_resources.items()
        }
        return Response(response_data)
