from django.shortcuts import redirect
from user.models import Member

class AllowTeamCreationMixin:
    allow_team_creation = True

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if user.is_authenticated:
            member = Member.objects.filter(user=user, acceptance_status=True).distinct()
            try:
                team = member.first().team 
                member_count = Member.objects.filter(team=team, acceptance_status=True).distinct().count()
            except:
                member_count = 0

            self.allow_team_creation = member_count < 3
            if not self.allow_team_creation:
                return redirect("index")

        return super().dispatch(request, *args, **kwargs)
