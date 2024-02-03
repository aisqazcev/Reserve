from django.contrib import admin
from .models import Booking, Building, Campus, Equipment, Space, Space_item, Room, Desk, CustomUser

admin.site.register(Booking)
admin.site.register(Space)
admin.site.register(Space_item)
admin.site.register(Room)
admin.site.register(Desk)
admin.site.register(Equipment)
admin.site.register(CustomUser)
admin.site.register(Campus)
admin.site.register(Building)
