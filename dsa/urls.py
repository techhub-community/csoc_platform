from django.urls import path

from .views import TopicListCreateAPIView, ProblemListCreateAPIView, StatusListCreateAPIView, ProblemStatusListCreateAPIView

app_name = 'dsa'


urlpatterns = [
    path('topic/', TopicListCreateAPIView.as_view(), name='topic-list-create'),
    path('problem/', ProblemListCreateAPIView.as_view(), name='problem-list-create'),
    path('status/', StatusListCreateAPIView.as_view(), name='status-list-create'),
    path('problem-status/', ProblemStatusListCreateAPIView.as_view(), name='problem-status-list-create'),
]
