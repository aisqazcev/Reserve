from rest_framework import serializers
from .models import Booking, Space, Location, Room, Desk

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'space', 'date', 'start_time', 'end_time', 'user')

class SpacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ('id', 'name', 'location', 'image', 'type', 'equipment', 'occupied')

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('id', 'name', 'institution', 'general_info', 'schedule', 'services', 'geodata', 'web', 'email', 'phone', 'image')

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'name', 'location', 'image', 'type', 'equipment', 'occupied', 'capacity')

class DeskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Desk
        fields = ('id', 'name', 'location', 'image', 'type', 'equipment', 'occupied', 'nearby_pl')
    
