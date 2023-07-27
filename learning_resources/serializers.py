from rest_framework import serializers

from .models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ('domain', 'topic', 'name', 'link')

    def to_representation(self, instance):
        grouped_resources = {}
        for resource in instance:
            domain = resource['domain']
            topic = resource['topic']
            if domain not in grouped_resources:
                grouped_resources[domain] = []
            existing_topic = next(
                (item for item in grouped_resources[domain] if item['topic'] == topic), None)
            if existing_topic:
                existing_topic['resources'].append({
                    'name': resource['name'],
                    'link': resource['link']
                })
            else:
                grouped_resources[domain].append({
                    'topic': topic,
                    'resources': [{
                        'name': resource['name'],
                        'link': resource['link']
                    }]
                })

        return grouped_resources
