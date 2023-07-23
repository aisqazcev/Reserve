from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

def user_directory_path(instance, filename):
    return 'reserve/{0}/{1}'.format(instance.name, filename)

class Location(models.Model):
    name = models.CharField(max_length=250)
    institution = models.CharField(max_length=250)
    general_info = models.TextField(null=False)
    schedule = models.TextField(null=False)
    services = models.TextField(null=False)
    geodata = models.TextField(null=False)
    web = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=250)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

class Equipment(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=False)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)

class Space(models.Model):

    option = (
        ('desk', 'Desk'),
        ('room', 'Room'),
    )

    name = models.CharField(max_length=250)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)    
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    equipment = models.ManyToManyField(Equipment, blank=True)
    occupied = models.BooleanField(default=False)

class Room(Space):
    capacity = models.IntegerField()
    type = models.CharField(max_length=10, choices=Space.option, default='room')


class Desk(Space):
    nearby_pl = models.ManyToManyField('self', blank=True)
    type = models.CharField(max_length=10, choices=Space.option, default='desk')

class Booking(models.Model):
    space = models.OneToOneField(Space, blank=False, null=False, on_delete=models.CASCADE)
    date = models.DateField() 
    start_time = models.TimeField()
    end_time = models.TimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
