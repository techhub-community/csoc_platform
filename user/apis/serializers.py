from rest_framework import serializers

from user.models import *


class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member  
        fields = ['id', 'user', 'team']  


class UserRetrieveSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'email', 'usn', 'phone_number',
                  'techstack', 'proficiency', 'first_name', 'last_name', 'team_members']

    def get_team_members(self, instance):
        team_member_ids = instance.get_team_member_ids()
        team_members_data = Member.objects.filter(id__in=team_member_ids)
        return MemberSerializer(team_members_data, many=True).data

