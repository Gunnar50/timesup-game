from rest_framework import serializers
from .models import Room, User

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__" 
        
class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ("words_per_user",)
        
class UpdateRoomSerializer(serializers.ModelSerializer):
    code = serializers.CharField(validators=[])
    
    class Meta:
        model = Room
        fields = ("words_per_user", "code")
        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", )
