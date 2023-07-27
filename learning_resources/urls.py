from django.urls import path

from .views import ResourceListCreateAPIView


urlpatterns = [
    path('', ResourceListCreateAPIView.as_view(), name='resource_list_create'),
]
