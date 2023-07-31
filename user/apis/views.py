from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from user.apis.serializers import UserRetrieveSerializer


class UserRetrieveView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
