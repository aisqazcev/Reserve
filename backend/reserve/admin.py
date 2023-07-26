from django.contrib import admin
from .models import Booking, Equipment, Space, Location, Room, Desk

admin.site.register(Booking)
admin.site.register(Space)
admin.site.register(Location)
admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(Equipment)