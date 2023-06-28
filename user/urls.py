from django.urls import path

from .views import (
    UserRegisterView, 
    UserLoginView, 
    UserLogoutView, 
    UserCreateTeamView, 
    UserProfileView,
    AcceptInviteView,
    RejectInviteView,
    EmailVerificationView,
    ClearSessionDataView
    )

app_name = 'user'

urlpatterns = [
    # path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('profile/', UserProfileView.as_view(template_name='account/profile.html'), name='profile'),
    path('create/team/', UserCreateTeamView.as_view(), name='create_team'),
    path('invite/accept/<int:pk>/', AcceptInviteView.as_view(), name='invite_accept'),
    path('invite/decline/<int:pk>/', RejectInviteView.as_view(), name='invite_decline'),
    path('verify-email/<str:token>/', EmailVerificationView.as_view(), name='email_verification'),
    path('session/data/clear/', ClearSessionDataView.as_view(), name='clear_session_data')
]
