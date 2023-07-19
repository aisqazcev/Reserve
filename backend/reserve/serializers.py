from rest_framework import serializers
from .models import Post, Booking, Spaces

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'title', 'image', 'description', 'content', 'slug', 'published', 'author', 'status')


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ('id', 'space', 'date', 'start_time', 'end_time', 'user', 'pplNumber')

class SpacesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Spaces
        fields = ('id', 'name', 'image', 'type')
