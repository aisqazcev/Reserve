from enum import Enum
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.conf import settings

def user_directory_path(instance, filename):
    return 'reserve/{0}/{1}'.format(instance.name, filename)

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, username, name, password=None, **extra_fields):
        if not username:
            raise ValueError('The username field must be set')
        
        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, name, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=150, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name']

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    space_item_id = models.ForeignKey(Space_item, blank=True, null=True, on_delete=models.CASCADE)
    date = models.DateField() 
    start_time = models.TimeField()
    end_time = models.TimeField()