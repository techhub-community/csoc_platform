from rest_framework import serializers

from user.models import *


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member  
        fields = ['id', 'user', 'team']  


class UserRetrieveSerializer(serializers.ModelSerializer):
    team_members = MemberSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'usn', 'phone_number',
                  'techstack', 'proficiency', 'first_name', 'last_name', 'team_members']

