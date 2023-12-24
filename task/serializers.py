from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    task_status = serializers.SerializerMethodField()

    def get_task_status(self, instance):
        user = self.context['request'].user
        return instance.get_task_status(user)
    
    class Meta:
        model = Task
        fields = ["task_name", "team", "detail", "task_status"]


class ProgressSerializer(serializers.Serializer):
    progress = serializers.FloatField()