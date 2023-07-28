from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated

from user.models import User
from user.apis.serializers import UserRetrieveSerializer


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj == request.user


class UserRetrieveView( generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsOwner]
    lookup_field = 'id'
