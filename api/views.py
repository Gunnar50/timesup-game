from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse


# Create your views here.
class RoomView(generics.ListAPIView):
    # retrive all instances of the Room models
    queryset = Room.objects.all()
    # serialize the class
    serializer_class = RoomSerializer
    
class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwargs = "code" # code matches the code variable in Room class models.py
    
    def get(self, request, format=None):
        # use requests.GET -> for GET requests
        code = request.GET.get(self.lookup_url_kwargs)
        if code != None:
            query_room = Room.objects.filter(code=code)
            if query_room.exists():
                room = query_room[0]
                data = RoomSerializer(room).data
                data["is_host"] = self.request.session.session_key == room.host
                return Response(data, status=status.HTTP_200_OK)
            return Response({"Room Not Found": "Invalid Room Code."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request": "Code parameter not found in request."}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwargs = "code"
    
    def post(self, request, format=None):
        # if current user does not have an active session with the server
        if not self.request.session.exists(self.request.session.session_key):
            # create a session
            self.request.session.create()
            
        # request.data -> use data for post requests.
        code = request.data.get(self.lookup_url_kwargs)
        if code:
            query_room_result = Room.objects.filter(code=code)
            if query_room_result.exists():
                room = query_room_result[0]
                
                # this new item room code is to check later if the user reconnect to the app then the user
                # do not need to type the room code again
                self.request.session["room_code"] = code
                
                return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)
            
            return Response({"Room Not Found": "Invalid Room Code."}, status=status.HTTP_404_NOT_FOUND)
            
        return Response({"Bad Request": "Code parameter not found in request."}, status=status.HTTP_400_BAD_REQUEST)



class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer
    
    def post(self, request, format=None):
        # if current user does not have an active session with the server
        if not self.request.session.exists(self.request.session.session_key):
            # create a session
            self.request.session.create()
            
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # create a room
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            host = self.request.session.session_key
            queryset = Room.objects.filter(host=host)
            
            # if the room already exists we dont want to create a new room
            if queryset.exists():
                # grab the active room and update its settings
                room = queryset[0] 
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
                
                # this new item room code is to check later if the user reconnect to the app then the user
                # do not need to type the room code again
                self.request.session["room_code"] = room.code
                
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            
            # if not updating, then create a new room
            else:
                room = Room(host=host, guest_can_pause=guest_can_pause, votes_to_skip=votes_to_skip)
                room.save()
                
                # this new item room code is to check later if the user reconnect to the app then the user
                # do not need to type the room code again
                self.request.session["room_code"] = room.code
                
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
                
        return Response(RoomSerializer(room).data, status=status.HTTP_400_BAD_REQUEST)
    
    
class UserInRoom(APIView):
    def get(self, request, format=None):
        # if current user does not have an active session with the server
        if not self.request.session.exists(self.request.session.session_key):
            # create a session
            self.request.session.create()
        data = {
            "code": self.request.session.get("room_code")
        }
        return JsonResponse(data, status=status.HTTP_200_OK)
    
    
class ExitRoom(APIView):
    def post(self, request, format=None):
        if "room_code" in self.request.session:
            self.request.session.pop("room_code")
            host_id = self.request.session.session_key
            query_room_results = Room.objects.filter(host=host_id)
            if query_room_results.exists():
                room = query_room_results[0]
                room.delete()
                
        return Response({"Message": "Success"}, status=status.HTTP_200_OK)
    
    
class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer
    
    def patch(self, request, format=None):
        # if current user does not have an active session with the server
        if not self.request.session.exists(self.request.session.session_key):
            # create a session
            self.request.session.create()
        

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            guest_can_pause = serializer.data.get("guest_can_pause")
            votes_to_skip = serializer.data.get("votes_to_skip")
            code = serializer.data.get("code")
            
            queryset_room = Room.objects.filter(code=code)
            if not queryset_room.exists():
                return Response({"message": "Room not found."}, status=status.HTTP_404_NOT_FOUND)
            
            room = queryset_room[0]
            
            # check if the current session key is the same as the host, meaning the user trying to update the room is the host
            if self.request.session.session_key == room.host:
                room.guest_can_pause = guest_can_pause
                room.votes_to_skip = votes_to_skip
                room.save(update_fields=["guest_can_pause", "votes_to_skip"])
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            
            return Response({"Message": "Not host"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"Bad Request": "Invalid Data."}, status=status.HTTP_400_BAD_REQUEST)
    
    