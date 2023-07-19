from django.urls import path
from .views import PostListView, PostShowView, BookingListView, BookingShowView, SpacesListView, SpacesShowView 

app_name="reserve"

urlpatterns = [
    path('posts/', PostListView.as_view(), name='post-list'),
    path('posts/<int:post_id>/', PostShowView.as_view(), name='post-show'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/', BookingShowView.as_view(), name='booking-show'),
    path('spaces/', SpacesListView.as_view()),
    path('spaces/<int:space_id>/', SpacesShowView.as_view()),
    
]