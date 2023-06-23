from django.urls import path

from .views import UserRegisterView, UserLoginView

app_name = 'user'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login')
]
