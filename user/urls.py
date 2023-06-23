from django.urls import path

from .views import UserRegisterView, UserLoginView, UserLogoutView, UserCreateTeamView

app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('create/team/', UserCreateTeamView.as_view(), name='create_team')
]
