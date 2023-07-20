from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from .serializers import WaitingRoomSerializer
from .models import WaitingRoom


class WaitingRoomView(CreateAPIView):
    queryset = WaitingRoom.objects.all()
    serializer_class = WaitingRoomSerializer
    
    
    
    
    