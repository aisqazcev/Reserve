from django.urls import path
from .views import BookingListView, BookingShowView, EquipmentManagementView, EquipmentShowView, SpaceListView, SpaceShowView, LocationManagementView, LocationShowView, RoomListView, RoomShowView, DeskListView, DeskShowView

app_name="reserve"

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/', BookingShowView.as_view(), name='booking-show'),
    path('space/', SpaceListView.as_view()),
    path('space/<int:space_id>/', SpaceShowView.as_view()),
    path('room/', RoomListView.as_view()),
    path('room/<int:room_id>/', RoomShowView.as_view()),
    path('desk/', DeskListView.as_view()),
    path('desk/<int:desk_id>/', DeskShowView.as_view()),
    path('location/', LocationManagementView.as_view()),
    path('location/<int:location_id>/', LocationShowView.as_view()),
    path('location/create/', LocationManagementView.as_view(), name='location-create'),
    path('equipment/', EquipmentManagementView.as_view()),
    path('equipment/<int:location_id>/', EquipmentShowView.as_view()),
    
]