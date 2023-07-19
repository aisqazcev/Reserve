from django.shortcuts import get_object_or_404, render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Post, Booking, Spaces
from .serializers import PostSerializer, BookingSerializer, SpacesSerializer

class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.postObject.all()
        serializer = PostSerializer(posts, many=True)

        return Response(serializer.data)


class PostShowView(APIView):
    def get(self, request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id = post_id)
        serializer = PostSerializer(post)

        return Response(serializer.data)
    
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
    
class SpacesListView(APIView):
    def get(self, request, *args, **kwargs):
        spaces = Spaces.objects.all()
        serializer = SpacesSerializer(spaces, many=True)

        return Response(serializer.data)
    
class SpacesShowView(APIView):
    def get(self, request, space_id, *args, **kwargs):
        space = get_object_or_404(Spaces, id = space_id)
        serializer = SpacesSerializer(space)

        return Response(serializer.data)