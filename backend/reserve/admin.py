from django.contrib import admin
from .models import Booking, Space, Location, Room, Desk

admin.site.register(Booking)
admin.site.register(Space)
admin.site.register(Location)
admin.site.register(Room)
admin.site.register(Desk)
