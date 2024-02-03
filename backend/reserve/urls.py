from django.urls import path
from .views import BookingListView, BookingManagementView, BuildingByCampusView, BuildingDetailstView, BuildingListView, CampusDetailstView, CampusListView, PasswordChangeView, RegisterView, BookingShowView, EquipmentManagementView, EquipmentShowView, LoginView, LogoutView, SpaceItemListView, SpaceShowView, SpaceManagementView, SpaceShowView, RoomListView, RoomShowView, DeskListView, DeskShowView, SpacesByBuildingView, UserView, search_spaces

app_name="reserve"

urlpatterns = [
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
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserView.as_view(), name='get_user_data'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),

    path('campus/', CampusListView.as_view(), name='campus-list'),
    path('campus/<int:campus_id>/', CampusDetailstView.as_view(), name='campus-details'),
    path('campus/<int:campus_id>/buildings/', BuildingByCampusView.as_view(), name='building_by_campus'),


    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('building/<int:building_id>/', BuildingDetailstView.as_view(), name='building-details'),
    path('building/<int:building_id>/spaces/', SpacesByBuildingView.as_view(), name='spaces_by_building'),

    path('booking/', BookingManagementView.as_view(), name='booking'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),

    path('search_spaces/', search_spaces, name='search_spaces'),
    
]