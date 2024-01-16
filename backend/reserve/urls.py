from django.urls import path
from .views import BookingListView, BookingManagementView, BookingShowView, BuildingListView, EquipmentManagementView, EquipmentShowView, LoginView, RegisterView, SpaceItemListView, SpaceShowView, SpaceManagementView, SpaceShowView, RoomListView, RoomShowView, DeskListView, DeskShowView

app_name="reserve"

urlpatterns = [
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:booking_id>/', BookingShowView.as_view(), name='booking-show'),
    path('space/', SpaceItemListView.as_view()),
    path('space/<int:space_id>/', SpaceShowView.as_view()),
    path('room/', RoomListView.as_view()),
    path('room/<int:room_id>/', RoomShowView.as_view()),
    path('desk/', DeskListView.as_view()),
    path('desk/<int:desk_id>/', DeskShowView.as_view()),
    path('location/', SpaceManagementView.as_view()),
    path('location/<int:location_id>/', SpaceShowView.as_view()),
    path('location/create/', SpaceManagementView.as_view(), name='location-create'),
    path('equipment/', EquipmentManagementView.as_view()),
    path('equipment/<int:location_id>/', EquipmentShowView.as_view()),

    path('login/', LoginView.as_view(), name='login'),

    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('booking/', BookingManagementView.as_view(), name='booking'),
    
]