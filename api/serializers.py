from rest_framework import serializers
from .models import WaitingRoom

class WaitingRoomSerializer(serializers.ModelSerializer):    
    class Meta:
        model = WaitingRoom
        fields = "__all__"
        
        
        
        
# class CreateRoomSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WaitingRoom
#         fields = ("guest_can_pause", "votes_to_skip")
        
# class UpdateRoomSerializer(serializers.ModelSerializer):
#     code = serializers.CharField(validators=[])
    
#     class Meta:
#         model = WaitingRoom
#         fields = ("guest_can_pause", "votes_to_skip", "code")