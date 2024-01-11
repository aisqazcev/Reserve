from django.contrib import admin
from .models import Booking, Equipment, Space, Space_item, Room, Desk

admin.site.register(Booking)
admin.site.register(Space)
admin.site.register(Space_item)
admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(Equipment)