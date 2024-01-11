from enum import Enum
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'reserve/{0}/{1}'.format(instance.name, filename)


# "Sala de estudio"
class Space(models.Model):
    name = models.CharField(max_length=250)
    building_name = models.CharField(max_length=250)
    capacity = models.IntegerField()
    general_info = models.TextField(null=False)
    schedule = models.TextField(null=False)
    services = models.TextField(null=False)
    address = models.TextField(null=False)
    web = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)    

class Equipment(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

class SeatStatus(Enum):
    FREE = 0
    RESERVED = 1
    EXPIRED = 2
    DISABLED = 3

class Space_item(models.Model): 
    space_id = models.ForeignKey(Space, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    equipment_id = models.ManyToManyField(Equipment, blank=True)
    seat_status = models.IntegerField(default=0, choices=[(status.value, status.name) for status in SeatStatus])


class Room(Space_item):
    capacity = models.IntegerField()

class Desk(Space_item):
    nearby_pl = models.ManyToManyField('self', blank=True)

class Booking(models.Model):
    user_id = models.ForeignKey(User, null= False, on_delete=models.CASCADE)
    space_item_id = models.ForeignKey(Space_item, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField() 
    start_time = models.TimeField()
    end_time = models.TimeField()

