from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Space, Location, Room, Desk
from .serializers import BookingSerializer, SpacesSerializer

class LocationListView(APIView):
    def get(self, request, *args, **kwargs):
        locations = Location.objects.all()
        serializer = SpacesSerializer(locations, many=True)

        return Response(serializer.data)
    
class LocationShowView(APIView):
    def get(self, request, location_id, *args, **kwargs):
        location = get_object_or_404(Location, id = location_id)
        serializer = SpacesSerializer(location)

        return Response(serializer.data)

##########################################################################################

class SpaceListView(APIView):
    def get(self, request, *args, **kwargs):
        spaces = Space.objects.all()
        serializer = SpacesSerializer(spaces, many=True)

        return Response(serializer.data)
    
class SpaceShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id = space_id)
        serializer = SpacesSerializer(space)

        return Response(serializer.data)
    
##########################################################################################

class RoomListView(APIView):
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        serializer = SpacesSerializer(rooms, many=True)

        return Response(serializer.data)

class RoomShowView(APIView):
    def get(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id = room_id)
        serializer = SpacesSerializer(room)

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
        serializer = SpacesSerializer(desks, many=True)

        return Response(serializer.data)
    
class DeskShowView(APIView):
    def get(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id = desk_id)
        serializer = SpacesSerializer(desk)

        return Response(serializer.data)


