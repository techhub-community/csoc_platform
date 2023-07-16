from django.urls import path

from .views import ContestListCreateAPIView, ParticipateContestAPIView

app_name = 'contest'


urlpatterns = [
    path('contest/', ContestListCreateAPIView.as_view(), name='contest-list-create'),
    path('participation/', ParticipateContestAPIView.as_view(), name='participation-list-create'),
   
]
