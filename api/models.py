from django.db import models
import string
import random

def generate_unique_code():
    length = 6
    while True:
        code = "".join(random.choices(string.ascii_uppercase, k=length))
        # returns a list with all objects that meet code=code
        # .count() to count how many there are. if is 0 means is unique
        if WaitingRoom.objects.filter(code=code).count() == 0:
            break
        
    return code

# Create your models here.
# models are the tables of the database
# these are the fields that will hep with the creationg of the records for the database

class WaitingRoom(models.Model):
    # code is the code to be shared for the room
    code = models.CharField(max_length=8, default=generate_unique_code, unique=True)
    # host is the host of the room, unique mean can only have one host
    host = models.CharField(max_length=50, unique=True)
    words_per_user = models.IntegerField(null=False, default=3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    
    