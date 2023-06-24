from typing import Any, Dict
from django.views.generic import TemplateView
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
    

class IndexTemplateView(AllowTeamCreationMixin, TemplateView):
    template_name='landing/index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['allow_team_creation'] = self.allow_team_creation
        return context
    