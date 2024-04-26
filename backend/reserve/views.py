import random
import secrets
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.cache import cache
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password




from .models import (
    Booking,
    Building,
    Campus,
    CustomUser,
    Equipment,
    Space,
    Room,
    Desk,
    Space_item,
)
from .serializers import (
    BookingSerializer,
    CustomUserSerializer,
    EquipmentSerializer,
    SpaceSerializer,
    RoomSerializer,
    DeskSerializer,
    BuildingSerializer,
    CampusSerializer,
    CustomUserSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
)
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
    HTTP_500_INTERNAL_SERVER_ERROR as ST_500
)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data.get("username_or_email", "")
        password = serializer.validated_data.get("password", "")

        if "@" in username_or_email:
            user = CustomUser.objects.filter(email=username_or_email).first()
        else:
            user = CustomUser.objects.filter(username=username_or_email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.pk, "username": user.username}
            )

        return Response(
            {"detail": "Credenciales inválidas"}, status=status.HTTP_401_UNAUTHORIZED
        )
    
@csrf_exempt
def change_pass_email(request, *args, **kwargs):
    try:
        data = json.loads(request.body.decode('utf-8'))
        email = data.get('email', '')
        username = CustomUser.objects.get(email=email).username
        user = CustomUser.objects.get(email=email)
        new_password = data.get('new_password', '')
        confirm_new_password = data.get('confirm_new_password', '')

        if new_password != confirm_new_password:
            return JsonResponse({"detail": "Las nuevas contraseñas no coinciden."}, status=400)
        
        else: 
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            return JsonResponse({"detail": "Contraseña cambiada exitosamente."}, status=200)
        
    except CustomUser.DoesNotExist:
        return JsonResponse({"detail": "Usuario no encontrado."}, status=404)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)
    
@csrf_exempt
def send_recovery_email(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        recipient_email = data.get('email', '')
        
        if CustomUser.objects.filter(email=recipient_email).exists():
            subject = 'Restauración de contraseña'
            verification_code = secrets.token_hex(4)
            message = f'¡Hola! Entra en este enlace para recuperar tu contraseña: {verification_code}. Por favor, no responda este correo.'
            from_email = 'seateasy8@gmail.com'

            cache.set(f'verification_code_{recipient_email}', verification_code, timeout=600)
            
            send_mail(subject, message, from_email, [recipient_email])

            return JsonResponse({'message': 'Correo enviado con éxito.', 'verification_code':cache.get(f'verification_code_{recipient_email}')})
        else:
            return JsonResponse({'error': 'El correo electrónico no está asociado a ningún usuario registrado.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

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
                raise AuthenticationFailed("No token provided")

        except Exception as e:
            return Response(
                {"detail": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST
            )
class RegisterView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "Usuario registrado exitosamente"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def enviar_correo_vista(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        recipient_email = data.get('email', '')
        subject = 'Verificación del registro'
        verification_code = secrets.token_hex(4)
        message = f'¡Hola! Este es tu código de verificación para confirmar el registro: {verification_code}. Por favor, no responda este correo.'
        from_email = 'seateasy8@gmail.com'

        cache.set(f'verification_code_{recipient_email}', verification_code, timeout=600)

        send_mail(subject, message, from_email, [recipient_email])

        return JsonResponse({'message': 'Correo enviado con éxito.'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def verificar_codigo(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
        recipient_email = data.get('email', '')
        verification_code = data.get('verificationCode', '')

        verification_code_cached = cache.get(f'verification_code_{recipient_email}')
       
        if verification_code == verification_code_cached:
            return JsonResponse({'valid': True})
        else:
            return JsonResponse({'valid': False, 'error': 'Código de verificación inválido'})

    except CustomUser.DoesNotExist:
        return JsonResponse({'valid': False, 'error': 'Usuario no encontrado'})
    except Exception as e:
        return JsonResponse({'valid': False, 'error': str(e)}, status=500)
@authentication_classes([TokenAuthentication])
class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        data = {
            "name": user.name if user.name else "Nombre Desconocido",
            "username": (
                user.get_username() if user.get_username() else "Username Desconocido"
            ),
        }
        return Response(data)


@authentication_classes([TokenAuthentication])
class PasswordChangeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data["current_password"]
            new_password = serializer.validated_data["new_password"]
            confirm_new_password = serializer.validated_data["confirm_new_password"]

            if not request.user.check_password(current_password):
                return Response(
                    {"detail": "Contraseña actual incorrecta."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if new_password != confirm_new_password:
                return Response(
                    {"detail": "Las nuevas contraseñas no coinciden."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.user.set_password(new_password)
            request.user.save()

            return Response(
                {"detail": "Contraseña cambiada exitosamente."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SpaceManagementView(APIView):

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
        space = get_object_or_404(Space, id=space_id)
        serializer = SpaceSerializer(space, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)

    def delete(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id=space_id)
        space.delete()
        return Response(data={"message": "Space deleted successfully"}, status=ST_200)
    
def occupation_actual(request, space_id):
        try:
            now = timezone.now()
            space = get_object_or_404(Space, id=space_id)
            start_time_filter = now - timezone.timedelta(hours=3)
            end_time_filter = now + timezone.timedelta(hours=3)
            overlapping_bookings = Booking.objects.filter(
                start_time__lte=end_time_filter,
                end_time__gte=start_time_filter,
                space=space
            )
            total_seats = space.capacity
            occupied_seats = overlapping_bookings.values('desk__id').distinct().count()
            occupancy_percentage = (occupied_seats / total_seats) * 100
         

            return JsonResponse({'occupationPercentage': occupancy_percentage})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)    


class SpaceShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id=space_id)
        serializer = SpaceSerializer(space)

        return Response(serializer.data)


class SpaceItemListView(APIView):
    def get(self, request, *args, **kwargs):
        space_items = Space_item.objects.all()
        serializer = SpaceSerializer(space_items, many=True)

        return Response(serializer.data)


class SpaceShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Space, id=space_id)
        serializer = SpaceSerializer(space)

        return Response(serializer.data)


class RoomManagementView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)

    def put(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomSerializer(room, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)

    def delete(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id=room_id)
        room.delete()
        return Response(data={"message": "Room deleted successfully"}, status=ST_200)


class RoomListView(APIView):
    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all()
        serializer = SpaceSerializer(rooms, many=True)

        return Response(serializer.data)


class RoomShowView(APIView):
    def get(self, request, room_id, *args, **kwargs):
        room = get_object_or_404(Room, id=room_id)
        serializer = RoomSerializer(room)

        return Response(serializer.data)


class DeskManagementView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = DeskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_201)
        return Response(data=serializer.errors, status=ST_409)

    def put(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id=desk_id)
        serializer = DeskSerializer(desk, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)

    def delete(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id=desk_id)
        desk.delete()
        return Response(data={"message": "Desk deleted successfully"}, status=ST_200)


class DeskListView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        desks = Desk.objects.filter(space_id = space_id)
        serializer = DeskSerializer(desks, many=True)

        return Response(serializer.data)


class DeskShowView(APIView):
    def get(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id=desk_id)
        serializer = DeskSerializer(desk)

        return Response(serializer.data)


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
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)

    def delete(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=booking_id)
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
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking)

        return Response(serializer.data)
    
def find_available_seats(request):
    if request.method == 'GET':
   
        start_time_str = request.GET.get('start_time')
        duration_str = request.GET.get('duration')

        if not start_time_str or not duration_str:
            return JsonResponse({'error': 'Debes proporcionar la hora de inicio y la duración.'}, status=400)

        try:
            start_time_str = start_time_str.rstrip('Z').split('.')[0]
            start_time = datetime.fromisoformat(start_time_str)

            duration = timedelta(minutes=int(duration_str))
            end_time = start_time + duration
 
            overlapping_bookings = Booking.objects.filter(date=start_time.date()).filter(
                start_time__lt=end_time, end_time__gt=start_time
            )

      
            all_seats = Desk.objects.all()

            available_seats = []
            for seat in all_seats:
                is_available = True
                for booking in overlapping_bookings:
                    if seat.id == booking.desk.id:
                        is_available = False
                        break
                if is_available:
                    available_seats.append(seat)

            available_seats_ids = [seat.id for seat in available_seats]

            return JsonResponse({'available_seats': available_seats_ids})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


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
        equipment = get_object_or_404(Equipment, id=equipment_id)
        serializer = EquipmentSerializer(equipment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=ST_200)
        return Response(data=serializer.errors, status=ST_409)

    def delete(self, request, equipment_id, *args, **kwargs):
        equipment = get_object_or_404(Equipment, id=equipment_id)
        equipment.delete()
        return Response(
            data={"message": "Equipment deleted successfully"}, status=ST_200
        )


class EquipmentShowView(APIView):
    def get(self, request, equipment_id, *args, **kwargs):
        equipment = get_object_or_404(Equipment, id=equipment_id)
        serializer = EquipmentSerializer(equipment)
        return Response(serializer.data)


class CampusListView(APIView):
    def get(self, request, *args, **kwargs):
        campuses = Campus.objects.all()
        serializer = CampusSerializer(campuses, many=True)
        return Response(serializer.data)
    
class CampusDetailView(APIView):
    def get(self, request, campus_id, *args, **kwargs):
        campus = get_object_or_404(Campus, id=campus_id)
        serializer = CampusSerializer(campus)
        return Response({"id": campus.id, "campus_name": campus.campus_name})

class BuildingListView(APIView):
    def get(self, request, *args, **kwargs):
        campus_name = request.query_params.get("campus", None)

        if campus_name:
            buildings = Building.objects.filter(
                campus__campus_name=campus_name 
            ).select_related("campus")
        else:
            buildings = Building.objects.all().select_related("campus")

        serializer = BuildingSerializer(buildings, many=True)
        serialized_data = serializer.data

        return JsonResponse(serialized_data, safe=False)

class BuildingDetailstView(APIView):
    def get(self, request, building_id, *args, **kwargs):
        building = get_object_or_404(Building, id=building_id)
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

def find_available_spaces(request):
    if request.method == 'GET':
        start_time_str = request.GET.get('start_time')
        duration_str = request.GET.get('duration')
        building_id = request.GET.get('building_id')
        campus_id = request.GET.get('campus_id')

        if not start_time_str or not duration_str:
            return JsonResponse({'error': 'Debes proporcionar la hora de inicio y la duración.'}, status=400)

        try:            
            start_time_str = start_time_str.rstrip('Z').split('.')[0]
            start_time = datetime.fromisoformat(start_time_str)
            start_time = timezone.make_aware(start_time, timezone.get_current_timezone())
            duration = timedelta(minutes=int(duration_str))
            end_time = start_time + duration

            overlapping_bookings = Booking.objects.filter(date=start_time.date()).filter(
                start_time__lt=end_time, 
                end_time__gt=start_time,                
            )
            all_spaces = Space.objects.all()
            if campus_id:
                all_spaces = all_spaces.filter(building__campus_id=campus_id)

            if building_id:
                all_spaces = all_spaces.filter(building_id=building_id)

            available_spaces = []
            for space in all_spaces:
                available_desks = [desk.id for desk in space.space_item_set.filter(seat_status=0)]
                overlapping_desks = [booking.desk.id for booking in overlapping_bookings]
                is_available = bool(set(available_desks) - set(overlapping_desks))
                if is_available:
                    available_spaces.append(space)

            available_spaces_ids = [space.id for space in available_spaces]

            return JsonResponse({'available_spaces': available_spaces_ids})

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
def get_random_images(request):
    try:
        espacios_aleatorios = random.sample(list(Space.objects.all()), 3)
        urls_imagenes = [f"{settings.MEDIA_URL}{espacio.image}" if espacio.image else None for espacio in espacios_aleatorios]
       
        return JsonResponse({'urls_imagenes': urls_imagenes})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({'error': 'Error interno del servidor'}, status=500)
    