
from .models import Contest , Participation
from .serializers import ContestSerializer , ParticipationSerializer
from rest_framework import generics
from rest_framework.response import Response


# Create your views here.
class ContestListCreateAPIView(generics.ListCreateAPIView):
    queryset = Contest.objects.all()
    serializer_class = ContestSerializer

     

    def list(self, request, *args, **kwargs):
        return Response({'status': 'OK',
            
            'something': [{'name': 'something'}, {'name': 'something else'}]})

class ParticipateContestAPIView(generics.ListCreateAPIView):
    queryset = Participation.objects.all()
    serializer_class = ParticipationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)