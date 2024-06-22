import random
import secrets
import json
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import datetime, timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
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
from django.contrib.auth.hashers import make_password
from django.utils.html import strip_tags

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
    HTTP_409_CONFLICT as ST_409,
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
        data = json.loads(request.body.decode("utf-8"))
        email = data.get("email", "")
        username = CustomUser.objects.get(email=email).username
        user = CustomUser.objects.get(email=email)
        new_password = data.get("new_password", "")
        confirm_new_password = data.get("confirm_new_password", "")

        if new_password != confirm_new_password:
            return JsonResponse(
                {"detail": "Las nuevas contraseñas no coinciden."}, status=400
            )

        else:
            hashed_password = make_password(new_password)
            user.password = hashed_password
            user.save()
            return JsonResponse(
                {"detail": "Contraseña cambiada exitosamente."}, status=200
            )

    except CustomUser.DoesNotExist:
        return JsonResponse({"detail": "Usuario no encontrado."}, status=404)
    except Exception as e:
        return JsonResponse({"detail": str(e)}, status=500)


@csrf_exempt
def send_recovery_email(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        recipient_email = data.get("email", "")

        if CustomUser.objects.filter(email=recipient_email).exists():
            subject = "Restauración de contraseña"
            verification_code = secrets.token_hex(4)
            message = f"¡Hola! Entra en este enlace para recuperar tu contraseña: {verification_code}. Por favor, no responda este correo."
            from_email = "seateasy8@gmail.com"

            cache.set(
                f"verification_code_{recipient_email}", verification_code, timeout=600
            )

            send_mail(subject, message, from_email, [recipient_email])

            return JsonResponse(
                {
                    "message": "Correo enviado con éxito.",
                    "verification_code": cache.get(
                        f"verification_code_{recipient_email}"
                    ),
                }
            )
        else:
            return JsonResponse(
                {
                    "error": "El correo electrónico no está asociado a ningún usuario registrado."
                },
                status=400,
            )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


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
def send_email_view(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        recipient_email = data.get("email", "")
        subject = "Verificación del registro"
        verification_code = secrets.token_hex(4)
        message = f"¡Hola! Este es tu código de verificación para confirmar el registro: {verification_code}. Por favor, no responda este correo."
        from_email = "seateasy8@gmail.com"

        cache.set(
            f"verification_code_{recipient_email}", verification_code, timeout=600
        )

        send_mail(subject, message, from_email, [recipient_email])

        return JsonResponse({"message": "Correo enviado con éxito."})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
def verify_code(request):
    try:
        data = json.loads(request.body.decode("utf-8"))
        recipient_email = data.get("email", "")
        verification_code = data.get("verificationCode", "")

        verification_code_cached = cache.get(f"verification_code_{recipient_email}")

        if verification_code == verification_code_cached:
            return JsonResponse({"valid": True})
        else:
            return JsonResponse(
                {"valid": False, "error": "Código de verificación inválido"}
            )

    except CustomUser.DoesNotExist:
        return JsonResponse({"valid": False, "error": "Usuario no encontrado"})
    except Exception as e:
        return JsonResponse({"valid": False, "error": str(e)}, status=500)


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
            "profile_image": user.profile_image,
                    }
        return Response(data)


@authentication_classes([TokenAuthentication])
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            current_password = serializer.validated_data["current_password"]
            new_password = serializer.validated_data["new_password"]

            if not request.user.check_password(current_password):
                return Response(
                    {"detail": "Contraseña actual incorrecta."},
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
            space=space,
        )
        total_seats = space.capacity
        occupied_seats = overlapping_bookings.values("desk__id").distinct().count()
        occupancy_percentage = (occupied_seats / total_seats) * 100

        return JsonResponse({"occupationPercentage": occupancy_percentage})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)


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
        desks = Desk.objects.filter(space_id=space_id)
        serializer = DeskSerializer(desks, many=True)

        return Response(serializer.data)


class DeskShowView(APIView):
    def get(self, request, desk_id, *args, **kwargs):
        desk = get_object_or_404(Desk, id=desk_id)
        serializer = DeskSerializer(desk)

        return Response(serializer.data)




def send_booking_email(user_email, reservation_details):
    subject = 'Detalles de su reserva'

    reservation_date = reservation_details['date']
    start_time_str = f"{reservation_date}T{reservation_details['start_time']}:00+00:00"
    start_time_local = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S%z")
    end_time_local = start_time_local + timedelta(minutes=reservation_details['duration'])

    start_datetime_utc = start_time_local.strftime('%Y%m%dT%H%M%S')
    end_datetime_utc = end_time_local.strftime('%Y%m%dT%H%M%S')

    google_calendar_url = (
        f"https://www.google.com/calendar/render?action=TEMPLATE"
        f"&text=Reserva+en+{reservation_details['building_name']}"
        f"&details=Reserva+de+{reservation_details['desk_name']}+en+{reservation_details['building_name']}+sala+{reservation_details['space_name']}"
        f"&location={reservation_details['building_name']},+{reservation_details['space_name']}"
        f"&dates={start_datetime_utc}/{end_datetime_utc}"
    )

    html_message = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
        <div style="margin: 0 auto; padding: 20px; max-width: 600px; background-color: #ffffff; border: 1px solid #ddd; border-radius: 10px;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h2 style="color: #333;">¡Hola!</h2>
                <p style="font-size: 18px; color: #555;">Gracias por su reserva. Aquí están los detalles:</p>
            </div>
            <div style="margin-bottom: 20px;">
                <table style="width: 100%; border-collapse: collapse; margin-top: 10px; border: 1px solid #ddd;">
                    <tr style="background-color: #f2f2f2;">
                        <th style="border: 1px solid #ddd; padding: 8px;">Edificio</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Sala</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Asiento</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Fecha</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Hora de inicio</th>
                        <th style="border: 1px solid #ddd; padding: 8px;">Hora de finalización</th>
                    </tr>
                    <tr>
                        <td style="border: 1px solid #ddd; padding: 8px;">{reservation_details['building_name']}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{reservation_details['space_name']}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{reservation_details['desk_name']}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{start_time_local.strftime('%d-%m-%Y')}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{start_time_local.strftime('%H:%M')}</td>
                        <td style="border: 1px solid #ddd; padding: 8px;">{end_time_local.strftime('%H:%M')}</td>
                    </tr>
                </table>
            </div>
            <div style="text-align: center; margin-bottom: 20px;">
                <p style="font-size: 16px; color: #555;">No olvides cancelar tu reserva si no puedes asistir.</p>
                <p><a href="{google_calendar_url}" target="_blank" style="color: #007bff; text-decoration: none;">Añade tu reserva a tu calendario de Google</a></p>
                <p style="font-size: 16px; color: #555;">Gracias por usar SeatEasy.</p>
            </div>
            <div style="margin-top: 20px; font-size: 12px; color: #888; text-align: center;">
                Por favor, no responda este correo.
            </div>
        </div>
    </body>
    </html>
    """
    plain_message = strip_tags(html_message)
    from_email = 'seateasy8@gmail.com'
    
    try:
        send_mail(subject, plain_message, from_email, [user_email], html_message=html_message)
    except Exception as e:
        print(f"Error enviando email: {e}")

@authentication_classes([TokenAuthentication])
class BookingManagementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data["user"] = request.user.id

        start_time_str = request.data.get("start_time")
        duration_minutes = int(request.data.get("duration"))
        desk_id = request.data.get("desk")

        if not start_time_str or not duration_minutes or not desk_id:
            return Response(
                {"error": "Faltan datos necesarios para crear la reserva."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
            start_time = timezone.make_aware(start_time, timezone.utc)

            duration = timedelta(minutes=duration_minutes)
            end_time = start_time + duration

            overlapping_bookings_user = Booking.objects.filter(
                user=request.user, start_time__lt=end_time, end_time__gt=start_time
            )

            if overlapping_bookings_user.exists():
                return Response(
                    {"error": "Ya tienes una reserva en esta franja horaria."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            overlapping_bookings_desk = Booking.objects.filter(
                desk_id=desk_id, start_time__lt=end_time, end_time__gt=start_time
            )

            if overlapping_bookings_desk.exists():
                return Response(
                    {
                        "error": "Este asiento ya está reservado para este intervalo de tiempo."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            request.data["start_time"] = start_time.isoformat()
            request.data["end_time"] = end_time.isoformat()
            request.data["duration"] = duration

            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                booking = serializer.save()

                reservation_details = {
                    'building_name': booking.space.building.name_complete,
                    'space_name': booking.space.name,
                    'desk_name': booking.desk.name,
                    'date': booking.date,
                    'start_time': start_time.strftime("%H:%M"),
                    'duration': duration_minutes
                }
                send_booking_email(request.user.email, reservation_details)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError as e:
            return Response(
                {"error": f"Formato de fecha inválido: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

class FindAvailableSeatsView(APIView):
    def get(self, request, *args, **kwargs):
        start_time_str = request.GET.get("start_time")
        duration_str = request.GET.get("duration")
        space_id = request.GET.get("space_id")

        if not start_time_str or not duration_str or not space_id:
            return JsonResponse(
                {
                    "error": "Debes proporcionar la hora de inicio, la duración y el ID del espacio."
                },
                status=400,
            )

        try:
            start_time = datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
            if timezone.is_naive(start_time):
                start_time = timezone.make_aware(start_time, timezone.utc)

            duration = timedelta(minutes=int(duration_str))
            end_time = start_time + duration

            overlapping_bookings = Booking.objects.filter(
                space_id=space_id, start_time__lt=end_time, end_time__gt=start_time
            )

            all_seats = Desk.objects.filter(space_id=space_id)
            unavailable_seats_ids = overlapping_bookings.values_list(
                "desk_id", flat=True
            )
            available_seats = all_seats.exclude(id__in=unavailable_seats_ids)

            available_seats_ids = [seat.id for seat in available_seats]

            return JsonResponse({"available_seats": available_seats_ids})

        except ValueError as e:
            return JsonResponse(
                {"error": f"Formato de fecha inválido: {str(e)}"}, status=400
            )


@authentication_classes([TokenAuthentication])
class BookingListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            bookings = Booking.objects.filter(user=request.user)
            serialized_bookings = []
            for booking in bookings:
                serialized_booking = BookingSerializer(booking).data
                serialized_booking["start_time"] = booking.start_time.astimezone(
                    timezone.utc
                ).isoformat()
                serialized_booking["end_time"] = booking.end_time.astimezone(
                    timezone.utc
                ).isoformat()
                serialized_booking["duration"] = int(
                    booking.duration.total_seconds() // 60
                )  
                serialized_bookings.append(serialized_booking)

            return Response(serialized_bookings, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookingShowView(APIView):
    def get(self, request, booking_id, *args, **kwargs):
        booking = get_object_or_404(Booking, id=booking_id)
        serializer = BookingSerializer(booking)

        return Response(serializer.data)


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
        return Response(serializer.data)



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
    if request.method == "GET":
        start_time_str = request.GET.get("start_time")
        duration_str = request.GET.get("duration")
        building_id = request.GET.get("building_id")
        campus_id = request.GET.get("campus_id")

        if not start_time_str or not duration_str:
            return JsonResponse(
                {"error": "Debes proporcionar la hora de inicio y la duración."},
                status=400,
            )

        try:
            start_time_str = start_time_str.rstrip("Z").split(".")[0]
            start_time = datetime.fromisoformat(start_time_str)
            start_time = timezone.make_aware(
                start_time, timezone.get_current_timezone()
            )
            duration = timedelta(minutes=int(duration_str))
            end_time = start_time + duration

            overlapping_bookings = Booking.objects.filter(
                date=start_time.date()
            ).filter(
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
                available_desks = [
                    desk.id for desk in space.space_item_set.filter(seat_status=0)
                ]
                overlapping_desks = [
                    booking.desk.id for booking in overlapping_bookings
                ]
                is_available = bool(set(available_desks) - set(overlapping_desks))
                if is_available:
                    available_spaces.append(space)

            available_spaces_ids = [space.id for space in available_spaces]

            return JsonResponse({"available_spaces": available_spaces_ids})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)


def get_random_images(request):
    try:
        random_spaces = random.sample(list(Space.objects.all()), 3)
        urls_imagenes = [
            f"{settings.MEDIA_URL}{space.image}" if space.image else None
            for space in random_spaces
        ]

        return JsonResponse({"urls_imagenes": urls_imagenes})
    except Exception as e:
        print(f"Error: {str(e)}")
        return JsonResponse({"error": "Error interno del servidor"}, status=500)


@csrf_exempt
def send_incidence(request):
    if request.method == "POST":
        data = json.loads(request.body)
        subject = data.get("subject")
        message = data.get("message")
        equipment = data.get("equipment")
        campus = data.get("campus")
        building = data.get("building")
        space = data.get("space")
        desk = data.get("desk")

        equipment_name = get_object_or_404(Equipment, id=equipment).name
        campus_name = get_object_or_404(Campus, id=campus).campus_name
        building_name = get_object_or_404(Building, id=building).name_complete
        space_name = get_object_or_404(Space, id=space).name

        if desk != None:
            desk_name = get_object_or_404(Desk, id=desk).name
            message = f"Ha ocurrido un problema en: {campus_name}, {building_name}, {space_name}, asiento: {desk_name} \n\nEl equipamiento afectado es: {equipment_name}\n\nDescripción del problema: {message}"
        else:
            message = f"Ha ocurrido un problema en: {campus_name}, {building_name}, {space_name}\n\nEl equipamiento afectado es: {equipment_name}\n\nDescripción del problema: {message}"

        sender_email = "seateasy8@gmail.com"
        receiver_email = "olivasanchez14@hotmail.com"

        send_mail(subject, message, sender_email, [receiver_email])
        return JsonResponse(
            {"success": True, "message": "Correo electrónico enviado con éxito."}
        )
    return JsonResponse(
        {"success": False, "message": "Método no permitido."}, status=405
    )


@csrf_exempt
def find_nearby_seats(request):
    try:
        data = json.loads(request.body)
        desk_id = data.get("desk_id")
        current_desk = Desk.objects.get(pk=desk_id)
        nearby_desks = current_desk.nearby_pl.all()
        nearby_desk_ids = [desk.id for desk in nearby_desks]
        return JsonResponse({"nearby_seat_ids": nearby_desk_ids})
    except Exception as e:
        return JsonResponse({"El asiento no existe": str(e)}, status=400)


def get_desk_name(desk_id):
    try:
        desk = Desk.objects.get(id=desk_id)
        return desk.name
    except Desk.DoesNotExist:
        return "Nombre no disponible"
    except Exception as e:
        return str(e)

@csrf_exempt  
@authentication_classes([TokenAuthentication]) 
def invite(request):
    try:
        data = json.loads(request.body)
        invited_email = data.get('email')
        if request.method == 'POST':
            data = json.loads(request.body)
            invited_email = data.get('invited_email')
            current_user = data.get('user_data')
            user_log = current_user.get('name')
            reserve_data = data.get('booking_data')
            nearby_seats = data.get('nearby_seats', [])

            date = datetime.strptime(reserve_data['date'], "%Y-%m-%d")
            formatted_date = date.strftime("%d-%m-%Y")
            start_time_local = datetime.strptime(reserve_data['start_time'], "%Y-%m-%dT%H:%M:%S%z")
            print(start_time_local)
            end_time_local = datetime.strptime(reserve_data['end_time'], "%Y-%m-%dT%H:%M:%S%z")
            formatted_start_time = start_time_local.strftime("%H:%M")
            formatted_end_time = end_time_local.strftime("%H:%M")

            start_time_utc = start_time_local
            end_time_utc = end_time_local
            start_datetime_utc = start_time_utc.strftime('%Y%m%dT%H%M%S')
            print(start_datetime_utc)
            end_datetime_utc = end_time_utc.strftime('%Y%m%dT%H%M%S')

            nearby_desk_names = []
            for desk_id in nearby_seats:
                desk_name = get_desk_name(desk_id)
                nearby_desk_names.append(desk_name)
            
            nearby_seats_list = "<ul>" + "".join([f"<li>{name}</li>" for name in nearby_desk_names]) + "</ul>"
            
            if CustomUser.objects.filter(email=invited_email).exists():
                subject = 'Ey, ¿te sientas a mi lado?'

                google_calendar_url = (
                    f"https://www.google.com/calendar/render?action=TEMPLATE"
                    f"&text=Reserva+en+{reserve_data['name_complete']}"
                    f"&details=Reserva+de+{invited_email}+en+{reserve_data['name_complete']}"
                    f"&location={reserve_data['name_complete']},+{reserve_data['spaceName']}"
                    f"&dates={start_datetime_utc}/{end_datetime_utc}"
                )

                message = f"""
                <!DOCTYPE html>
                <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; background-color: #f9f9f9; margin: 0; padding: 0;">
                    <div style="margin: 0 auto; padding: 20px; max-width: 600px; background-color: #ffffff; border: 1px solid #ddd; border-radius: 10px;">
                        <div style="text-align: center; margin-bottom: 20px;">
                            <h2 style="color: #333;">¡Hola!</h2>
                            <p style="font-size: 18px; color: #555;">Tu compañero <strong>{user_log}</strong> te ha invitado a sentarte a su lado.</p>
                        </div>
                        <div style="margin-bottom: 20px;">
                            <p style="font-size: 16px; color: #555;">Aquí están los detalles de la reserva:</p>
                            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; border: 1px solid #ddd;">
                                <tr style="background-color: #f2f2f2;">
                                    <th style="border: 1px solid #ddd; padding: 8px;">Edificio</th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">Sala</th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">Fecha</th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">Hora de inicio</th>
                                    <th style="border: 1px solid #ddd; padding: 8px;">Hora de fin</th>
                                </tr>
                                <tr>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{reserve_data['name_complete']}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{reserve_data['spaceName']}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{formatted_date}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{formatted_start_time}</td>
                                    <td style="border: 1px solid #ddd; padding: 8px;">{formatted_end_time}</td>
                                </tr>
                            </table>
                        </div>
                        <div style="margin-bottom: 20px;">
                            <p style="font-size: 16px; color: #555;">Tienes estos asientos cercanos disponibles para reservar:</p>
                            {nearby_seats_list}
                        </div>
                        <div style="text-align: center; margin-bottom: 20px;">
                            <p style="font-size: 16px; color: #555;">Entra en <a href="https://seateasy-61465.web.app/" target="_blank" style="color: #007bff; text-decoration: none;">SeatEasy</a> y reserva tu asiento. ¡No te quedes sin tu sitio!</p>
                            <p><a href="{google_calendar_url}" target="_blank" style="color: #007bff; text-decoration: none;">Añadir al Calendario de Google</a></p>
                        </div>
                        <div style="margin-top: 20px; font-size: 12px; color: #888; text-align: center;">
                            Por favor, no responda este correo.
                        </div>
                    </div>
                </body>
                </html>
                """

                from_email = 'seateasy8@gmail.com'

                send_mail(subject, '', from_email, [invited_email], html_message=message)

                return JsonResponse({'message': 'Correo enviado con éxito.'})
            else:
                return JsonResponse({'error': 'El correo electrónico no está asociado a ningún usuario registrado.'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

from rest_framework.decorators import api_view, permission_classes

@csrf_exempt
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_profile_image(request):
    user = request.user
    profile_image_url = request.data.get('profile_image', None)
    if profile_image_url:
        print(profile_image_url)
        user.profile_image = profile_image_url
        user.save()
        return Response({"detail": "Imagen de perfil actualizada exitosamente."}, status=status.HTTP_200_OK)
    return Response({"detail": "No se proporcionó ninguna URL de imagen de perfil."}, status=status.HTTP_400_BAD_REQUEST)