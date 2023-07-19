from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    task_status = serializers.SerializerMethodField()

    def get_task_status(self, instance):
        return instance.get_task_status
    
    class Meta:
        model = Task
        fields = ["task_name", "team", "detail", "task_status"]
