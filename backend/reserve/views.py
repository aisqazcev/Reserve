from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
import json
from rest_framework import views
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Booking, Building, Equipment, Space, Room, Desk, Space_item
from .serializers import BookingSerializer, BuildingSerializer, EquipmentSerializer, SpaceSerializer, RoomSerializer, DeskSerializer
from rest_framework.status import (
    HTTP_200_OK as ST_200,
    HTTP_201_CREATED as ST_201,
    HTTP_403_FORBIDDEN as ST_403,
    HTTP_404_NOT_FOUND as ST_404,
    HTTP_409_CONFLICT as ST_409,
    HTTP_204_NO_CONTENT as ST_204,
    HTTP_400_BAD_REQUEST as ST_400,
    HTTP_205_RESET_CONTENT as ST_205,
    HTTP_401_UNAUTHORIZED as ST_401,
)
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.tokens import RefreshToken


class SpaceManagementView(APIView):
        
        #show all spaces
        def get(self, request, *args, **kwargs):
            spaces = Space.objects.all()
            serializer = SpaceSerializer(spaces, many=True)
    
            return Response(serializer.data)
        
        def post(self, request, *args, **kwargs):
            serializer = SpaceSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=ST_201)
            return Response(data=serializer.errors, status=ST_409)
        
        def put(self, request, space_id, *args, **kwargs):
            space = get_object_or_404(Space, id = space_id)
            serializer = SpaceSerializer(space, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=ST_200)
            return Response(data=serializer.errors, status=ST_409)
        
        def delete(self, request, space_id, *args, **kwargs):
            space = get_object_or_404(Space, id = space_id)
            space.delete()
            return Response(data={"message": "Space deleted successfully"}, status=ST_200)
   
class SpaceShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id = space_id)
        serializer = SpaceSerializer(space)

        return Response(serializer.data)    

##########################################################################################


class SpaceItemListView(APIView):
    def get(self, request, *args, **kwargs):
        space_items = Space_item.objects.all()
        serializer = SpaceSerializer(space_items, many=True)

        return Response(serializer.data)
    
class SpaceShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id = space_id)
        serializer = SpaceSerializer(space)

        return Response(serializer.data)
    
##########################################################################################

class RoomManagementView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)
    
    def put(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id = room_id)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)
    
    def delete(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id = room_id)
        room.delete()
        return Response(data={"message": "Room deleted successfully"}, status=ST_200)
        
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

class DeskManagementView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DeskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)
    
    def put(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id = desk_id)
        serializer = DeskSerializer(desk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)
    
    def delete(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id = desk_id)
        desk.delete()
        return Response(data={"message": "Desk deleted successfully"}, status=ST_200)
    
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


##########################################################################################    

class BookingManagementView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = BookingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)
    
    def put(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id = booking_id)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)
    
    def delete(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id = booking_id)
        booking.delete()
        return Response(data={"message": "Booking deleted successfully"}, status=ST_200)
    
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
class EquipmentManagementView(APIView):

    def get(self, request, *args, **kwargs):
        equipments = Equipment.objects.all()
        serializer = EquipmentSerializer(equipments, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = EquipmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)

    def put(self, request, equipment_id, *args, **kwargs):
        equipment = get_object_or_404(Equipment, id = equipment_id)
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)

    def delete(self, request, equipment_id, *args, **kwargs):
        equipment = get_object_or_404(Equipment, id = equipment_id)
        equipment.delete()
        return Response(data={"message": "Equipment deleted successfully"}, status=ST_200)

class EquipmentShowView(APIView):
    def get(self, request, equipment_id, *args, **kwargs):
        equipment = get_object_or_404(Equipment, id = equipment_id)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)
    

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response({'detail': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


#create BuildingListView
class BuildingListView(APIView):
    def get(self, request, *args, **kwargs):
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)

        return Response(serializer.data)