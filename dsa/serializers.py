from rest_framework import serializers
from .models import Topic, Problem, Problem_Status


class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'


class ProblemStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem_Status
        fields = '__all__'