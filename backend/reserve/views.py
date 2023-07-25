from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Space, Location, Room, Desk
from .serializers import BookingSerializer, SpaceSerializer, LocationSerializer, RoomSerializer, DeskSerializer
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
)

class LocationManagementView(APIView):
    
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)

        return Response(serializer.data)
    
    def post(self, request, *args, **kwargs):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)
    
    def put(self, request, location_id, *args, **kwargs):
        location = get_object_or_404(Location, id = location_id)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)
    
    def delete(self, request, location_id, *args, **kwargs):
        location = get_object_or_404(Location, id = location_id)
        location.delete()
        return Response(data={"message": "Location deleted successfully"}, status=ST_200)
    

class LocationShowView(APIView):
    def get(self, request, location_id, *args, **kwargs):
        location = get_object_or_404(Location, id = location_id)
        serializer = LocationSerializer(location)

        return Response(serializer.data)

##########################################################################################

class SpaceListView(APIView):
    def get(self, request, *args, **kwargs):
        spaces = Space.objects.all()
        serializer = SpaceSerializer(spaces, many=True)

        return Response(serializer.data)
    
class SpaceShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id = space_id)
        serializer = SpaceSerializer(space)

        return Response(serializer.data)
    
##########################################################################################

class RoomListView(APIView):
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True)

        return Response(serializer.data)

class RoomShowView(APIView):
    def get(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id = room_id)
        serializer = RoomSerializer(room)

        return Response(serializer.data)

##########################################################################################    
class BookingListView(APIView):
    def get(self, request, *args, **kwargs):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)

        return Response(serializer.data)

class BookingShowView(APIView):
    def get(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id = booking_id)
        serializer = BookingSerializer(booking)

        return Response(serializer.data)
    

##########################################################################################

class DeskListView(APIView):
    def get(self, request, *args, **kwargs):
        desks = Desk.objects.all()
        serializer = DeskSerializer(desks, many=True)

        return Response(serializer.data)
    
class DeskShowView(APIView):
    def get(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id = desk_id)
        serializer = DeskSerializer(desk)

        return Response(serializer.data)


