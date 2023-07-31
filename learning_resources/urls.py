from django.urls import path

from .views import ResourceListAPIView


urlpatterns = [
    path('', ResourceListAPIView.as_view(), name='resource_list'),
]
