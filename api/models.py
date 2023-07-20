from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        # returns a list with all objects that meet code=code
        # .count() to count how many there are. if is 0 means is unique
        if Room.objects.filter(code=code).count() == 0:
            break
        
    return code


class Room(models.Model):
    # code is the code to be shared for the room
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)    
    words_per_user = models.IntegerField(null=False, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    

class User(models.Model):
    username = models.CharField(max_length=50, unique=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    is_host = models.BooleanField(default=False)
    session_id = models.CharField(max_length=50, unique=True)
    
    