from django.urls import path

from django.views.generic import TemplateView

app_name = 'user'

urlpatterns = [
    path('register/', TemplateView.as_view(template_name='registration.html'), name='register')
]
