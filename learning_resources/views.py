import pandas as pd

from rest_framework.generics import ListAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response

from .models import Resource
from .serializers import ResourceSerializer
from user.apis.permissions import CustomPermissionMixin


class ResourceListAPIView(CustomPermissionMixin, ListAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    authentication_classes = [JWTAuthentication]

    def generate_grouped_resources(self):
        resources = Resource.objects.all().values_list('program__name', 'topic', 'description', 'link')
        df = pd.DataFrame.from_records(resources, columns=['program__name', 'topic', 'description', 'link'])
        grouped_df = df.groupby(['program__name', 'topic'])
        return [
            (program_name, topic, [{"description": row.description, "link": row.link} for row in group.itertuples(index=False)])
            for (program_name, topic), group in grouped_df
        ]

    def get(self, request, *args, **kwargs):
        grouped_resources = {
            program_name: [
                {"topic": topic, "resources": resources_list}
                for program_name, topic, resources_list in self.generate_grouped_resources()
            ]
            for program_name, topic, resources_list in self.generate_grouped_resources()
        }
        return Response(grouped_resources)
