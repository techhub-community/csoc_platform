from django.urls import path

from .views import (
    UserRegisterView, 
    UserLoginView, 
    UserLogoutView, 
    UserCreateTeamView, 
    UserProfileView
    )

app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(template_name='account/profile.html'), name='profile'),
    path('create/team/', UserCreateTeamView.as_view(), name='create_team')
]
