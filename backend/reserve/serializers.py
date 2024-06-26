import re
from .models import Booking
from datetime import datetime, timedelta
from django.utils import timezone
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import (
    Booking,
    Building,
    Campus,
    Equipment,
    Space,
    Space_item,
    Room,
    Desk,
    CustomUser,
)


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["id", "name", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("La contraseña debe tener al menos 8 caracteres.")
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r'[a-z]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un número.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("La contraseña debe contener al menos un carácter especial.")
        return value

    def validate(self, data):
        if data['new_password'] != data['confirm_new_password']:
            raise serializers.ValidationError("Las nuevas contraseñas no coinciden.")
        return data


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['id', 'user', 'campus', 'building', 'space', 'desk', 'date', 'start_time', 'duration', 'end_time']
    
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['start_time'] = instance.start_time.astimezone(timezone.utc).isoformat()
        ret['end_time'] = instance.end_time.astimezone(timezone.utc).isoformat()
        ret['duration'] = int(instance.duration.total_seconds() // 60) 
        return ret

class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = "__all__"


class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = "__all__"


class Space_itemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space_item
        fields = "__all__"


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = "__all__"


class DeskSerializer(serializers.ModelSerializer):
    nearby_desks_names = serializers.SerializerMethodField()

    class Meta:
        model = Desk
        fields = ['id', 'name', 'space_id', 'seat_status', 'nearby_desks_names', 'image']

    def get_nearby_desks_names(self, obj):
        nearby_desks = obj.nearby_pl.all()
        formatted_names = []
        for desk in nearby_desks:
            numbers = re.findall(r'\d+', desk.name)
            if numbers:
                desk_number = numbers[-1]
                first_letter = desk.name[0].upper()
                formatted_names.append(f"{first_letter}{desk_number}")
        return formatted_names
    
class CampusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Campus
        fields = '__all__'

class BuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Building
        fields = "__all__"

