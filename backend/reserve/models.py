from enum import Enum
import json
import os
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.conf import settings
from django.db.models.signals import post_migrate
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return "reserve/{0}/{1}".format(instance.name, filename)


class CustomUserManager(BaseUserManager):
    def create_user(self, username, name, password=None, **extra_fields):
        if not username:
            raise ValueError("The username field must be set")

        user = self.model(username=username, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, name, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=250)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = CustomUserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "username"]

    def __str__(self):
        return self.email


class Campus(models.Model):
    campus_name = models.CharField(max_length=250, unique=True)

    def __str__(self):
        return self.campus_name


class Building(models.Model):
    name = models.CharField(max_length=255, unique=True)
    name_complete = models.CharField(max_length=255)
    address = models.TextField(null=False)
    web = models.URLField(max_length=200)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=250)
    services = models.TextField(null=False)
    image = models.ImageField(blank=True, null=True)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

def load_building_data():
    json_file_path = os.path.join(settings.BASE_DIR, "reserve", "buildings_name.json")

    with open(json_file_path, "r", encoding="utf-8") as json_file:
        buildings_data = json.load(json_file)

        for building_data in buildings_data:
            campus_name = building_data.get("campus", "")

            unique_campus, _ = Campus.objects.get_or_create(campus_name=campus_name)

            existing_building = Building.objects.filter(
                name=building_data.get("name")
            ).first()

            if not existing_building:
                Building.objects.create(
                    name=building_data.get("name", ""),
                    name_complete=building_data.get("name_complete", ""),
                    address=building_data.get("address", ""),
                    web=building_data.get("web", ""),
                    email=building_data.get("email", ""),
                    phone=building_data.get("phone", ""),
                    services=building_data.get("services", ""),
                    image=building_data.get("image", ""),
                    campus=unique_campus,
                )


@receiver(post_migrate)
def load_building_data_after_migrate(sender, **kwargs):
    if sender.name == "reserve":
        load_building_data()


class Space(models.Model):
    name = models.CharField(max_length=250)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    capacity = models.IntegerField()
    general_info = models.TextField(null=False)
    schedule = models.TextField(null=False)
    image = models.ImageField(blank=True, null=True)


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
    seat_status = models.IntegerField(
        default=0, choices=[(status.value, status.name) for status in SeatStatus]
    )

class Room(Space_item):
    capacity = models.IntegerField()

class Desk(Space_item):
    nearby_pl = models.ManyToManyField("self", blank=True)

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    desk = models.ForeignKey(Desk, on_delete=models.CASCADE)
    date = models.DateField() 
    start_time = models.DateTimeField()  
    end_time = models.DateTimeField()  
