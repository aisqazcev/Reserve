from django.shortcuts import get_object_or_404
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import CampusSerializer, CustomUserSerializer, LoginSerializer, PasswordChangeSerializer
from rest_framework.response import Response
from .models import Booking, Building, Campus, CustomUser, Equipment, Space, Room, Desk, Space_item
from .serializers import BookingSerializer, CustomUserSerializer, EquipmentSerializer, SpaceSerializer, RoomSerializer, DeskSerializer, BuildingSerializer
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


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer  # Usa el nuevo serializador para el inicio de sesión

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data.get('username_or_email', '')
        password = serializer.validated_data.get('password', '')

        if '@' in username_or_email:
            user = CustomUser.objects.filter(email=username_or_email).first()
        else:
            user = CustomUser.objects.filter(username=username_or_email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})

        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


@authentication_classes([TokenAuthentication])
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if request.auth:
                request.auth.delete()
                logout(request)
                return Response(status=status.HTTP_200_OK)
            else:
                raise AuthenticationFailed('No token provided')
       
        except Exception as e:
            print(f"Error during logout: {e}")
            return Response({'detail': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'detail': 'Usuario registrado exitosamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
@authentication_classes([TokenAuthentication])
class UserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            'name': user.name if user.name else "Nombre Desconocido",
            'username': user.get_username() if user.get_username() else "Username Desconocido",
        }
        return Response(data)
    
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data['current_password']
            new_password = serializer.validated_data['new_password']
            confirm_new_password = serializer.validated_data['confirm_new_password']

            # Verificar la contraseña actual del usuario
            if not request.user.check_password(current_password):
                return Response({'detail': 'Contraseña actual incorrecta.'}, status=status.HTTP_400_BAD_REQUEST)

            # Verificar que la nueva contraseña y la confirmación coincidan
            if new_password != confirm_new_password:
                return Response({'detail': 'Las nuevas contraseñas no coinciden.'}, status=status.HTTP_400_BAD_REQUEST)

            # Cambiar la contraseña
            request.user.set_password(new_password)
            request.user.save()

            return Response({'detail': 'Contraseña cambiada exitosamente.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
##########################################################################################

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
@authentication_classes([TokenAuthentication])
class BookingManagementView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, *args, **kwargs):

        request.data['user'] = request.user.id
        
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
    
@authentication_classes([TokenAuthentication])
class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            bookings = Booking.objects.filter(user=request.user)
            serializer = BookingSerializer(bookings, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

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

class CampusListView(APIView):
    def get(self, request, *args, **kwargs):
        campus_list = Campus.objects.all()
        serializer = CampusSerializer(campus_list, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class CampusDetailstView(APIView):
    def get(self, request, campus_id, *args, **kwargs):
        campus = get_object_or_404(Campus, id = campus_id)
        serializer = CampusSerializer(campus)

        return Response(serializer.data)

class BuildingListView(APIView):
    def get(self, request, *args, **kwargs):
        buildings = Building.objects.all()
        serializer = BuildingSerializer(buildings, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
class BuildingDetailstView(APIView):
    def get(self, request, building_id, *args, **kwargs):
        building = get_object_or_404(Building, id = building_id)
        serializer = BuildingSerializer(building)

        return Response(serializer.data)
    
class BuildingByCampusView(APIView):
    def get(self, request, campus_id, *args, **kwargs):
        buildings = Building.objects.filter(campus_id=campus_id)
        serializer = BuildingSerializer(buildings, many=True)

        return Response(serializer.data)
    
class SpacesByBuildingView(APIView):
    def get(self, request, building_id, *args, **kwargs):
        spaces = Space.objects.filter(building_id=building_id)
        serializer = SpaceSerializer(spaces, many=True)

        return Response(serializer.data)
    
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def search_spaces(request):
    campus_id = request.GET.get('campus', None)
    building_id = request.GET.get('building', None)

    spaces = Space.objects.all()

    if campus_id:
        spaces = spaces.filter(building__campus__id=campus_id)
    if building_id:
        spaces = spaces.filter(building__id=building_id)

    serialized_spaces = SpaceSerializer(spaces, many=True)
    print(f"Spaces: ", serialized_spaces)
    return Response(serialized_spaces.data)


