from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer, UpdateRoomSerializer, UserSerializer, CreateUserSerializer
from .models import Room, User
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})


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
            session_id = self.request.session.session_key
            user_query = User.objects.filter(session_id=session_id)
            if user_query.exists():
                user = user_query[0]
                query_room = Room.objects.filter(code=code)
                if query_room.exists():
                    room = query_room[0]
                    if user.room == room:
                        data = RoomSerializer(room).data
                        data["is_host"] = user.is_host
                        return Response(data, status=status.HTTP_200_OK)
                    return Response({"Incorrect Room": "User Must Leave The Room First"}, status=status.HTTP_400_BAD_REQUEST)
                return Response({"Room Not Found": "Invalid Room Code"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"User Not Found": "User must joing a room first"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"Bad Request": "Code parameter not found in request."}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    def post(self, request, format=None):
        # if current user does not have an active session with the server
        session_id = self.request.session.session_key
        print(1, session_id)
        if self.request.session.exists(session_id):
            if User.objects.filter(session_id=session_id).exists():
                return Response({"Not Allowed": "User can only be in on room at one time."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        else:
            # create a session
            self.request.session.create()
            session_id = self.request.session.session_key
        print(2, session_id)
            
        # request.data -> use data for post requests.
        username = request.data.get("username")
        if User.objects.filter(username=username).exists():
            return Response({"Not Allowed": "Username Must Be Unique."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        code = request.data.get("code")
        if not code:
            return Response({"Bad Request": "Code parameter not found in request."}, status=status.HTTP_400_BAD_REQUEST)

        query_room = Room.objects.filter(code=code)
        if not query_room.exists():
            return Response({"Room Not Found": "Invalid Room Code."}, status=status.HTTP_404_NOT_FOUND)
        
        # this new item room code is to check later if the user reconnect to the app then the user
        # do not need to type the room code again
        self.request.session["room_code"] = code
        
        room = query_room[0]
        User.objects.create(username=username, session_id=session_id, room=room, is_host=False)
        
        return Response({"message": "Room Joined!"}, status=status.HTTP_200_OK)
        
       
            
class CreateRoomView(APIView):
    room_serializer_class = CreateRoomSerializer
    user_serializer_class = CreateUserSerializer
    
    def post(self, request, format=None):
        # if current user does not have an active session with the server
        if not self.request.session.exists(self.request.session.session_key):
            # create a session
            self.request.session.create()
        
        room_serializer = self.room_serializer_class(data=request.data)
        user_serializer = self.user_serializer_class(data=request.data)
        if room_serializer.is_valid() and user_serializer.is_valid():
            # create a room
            username = user_serializer.data.get("username")
            words_per_user = room_serializer.data.get("words_per_user")
            host_id = self.request.session.session_key
            queryset = User.objects.filter(session_id=host_id, is_host=True)
            
            # if the room already exists we dont want to create a new room
            if queryset.exists():
                # grab the active room and update its settings
                user = queryset[0]
                user.username = username
                room = user.room
                room.words_per_user = words_per_user
                user.save(update_fields=["username"])
                room.save(update_fields=["words_per_user"])
                
                # this new item room code is to check later if the user reconnect to the app then the user
                # do not need to type the room code again
                self.request.session["room_code"] = room.code
                
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            
            # if not updating, then create a new room
            else:
                room = Room(words_per_user=words_per_user)
                room.save()
                User.objects.create(username=username, session_id=host_id, room=room, is_host=True)
                
                # this new item room code is to check later if the user reconnect to the app then the user
                # do not need to type the room code again
                self.request.session["room_code"] = room.code
                
                return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
                
        return Response({"Bad Request": "Room Not Found"}, status=status.HTTP_400_BAD_REQUEST)
    
class GetUsersInRoom(APIView):
    def get(self, request, format=None):
        code = request.GET.get("code")
        room = Room.objects.filter(code=code)
        if room.exists():
            users = User.objects.filter(room=room[0])
            return Response(UserSerializer(users, many=True).data, status=status.HTTP_200_OK)
        else:
            return Response({"Bad Request": "Room Not Found"}, status=status.HTTP_404_NOT_FOUND)
    
    
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
            session_id = self.request.session.session_key
            query_user = User.objects.filter(session_id=session_id)
            if query_user.exists():
                user = query_user[0]
                if user.is_host:
                    room = query_user[0].room
                    room.delete()
                user.delete()
       
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
    
    