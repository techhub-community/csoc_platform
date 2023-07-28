from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    team_members = serializers.SerializerMethodField()

    def get_team_members(self, obj):
        return obj.get_team_member_ids()

    class Meta:
        model = User
        fields = fields = ['id', 'email', 'usn', 'phone_number',
                           'techstack', 'proficiency', 'first_name', 'last_name', 'team_members']
