from django.urls import path

from .views import TopicListCreateAPIView, ProblemListCreateAPIView, ProblemStatusListAPIView

app_name = 'dsa'


urlpatterns = [
    path('topic/', TopicListCreateAPIView.as_view(), name='topic_list_create'),
    path('problem/', ProblemListCreateAPIView.as_view(), name='problem_list_create'),
    path('problem/status/', ProblemStatusListAPIView.as_view(), name='problem_status_list'),
]
