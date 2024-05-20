from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import BookingListView, BookingManagementView, BuildingDetailstView, BuildingListView, CampusDetailView, CampusListView, FindAvailableSeatsView, PasswordChangeView, RegisterView, BookingShowView, EquipmentManagementView, EquipmentShowView, LoginView, LogoutView, SpaceItemListView, SpaceShowView, SpaceManagementView, SpaceShowView, RoomListView, RoomShowView, DeskListView, DeskShowView, SpacesByBuildingView, UserView, change_pass_email, find_available_spaces, find_nearby_seats, get_random_images, invite, occupation_actual, send_email_view, send_incidence, send_recovery_email, verify_code
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

app_name="reserve"

schema_view = get_schema_view(
   openapi.Info(
      title="Doc API",
      default_version='v1',
      description="API for the Seateasy project",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    path('bookings/<int:booking_id>/', BookingShowView.as_view(), name='booking-show'),
    path('spaces/', SpaceManagementView.as_view()),
    path('space/<int:space_id>/', SpaceShowView.as_view()),
    path('room/', RoomListView.as_view()),
    path('room/<int:room_id>/', RoomShowView.as_view()),
    path('<int:space_id>/desk/', DeskListView.as_view()),
    path('desk/<int:desk_id>/', DeskShowView.as_view()),

    path('equipment/', EquipmentManagementView.as_view()),
    path('equipment/<int:equipment_id>/', EquipmentShowView.as_view()),

    path('login/', LoginView.as_view(), name='login'),
    path('send_recovery/', send_recovery_email, name='send_recovery'),
    path('send_incidence/', send_incidence, name='send_incidence'),
    path('change_pass/', change_pass_email, name='change_pass'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserView.as_view(), name='get_user_data'),
    path('change-password/', PasswordChangeView.as_view(), name='change-password'),
    
    path('send_email/', send_email_view, name='send_email'),
    path('verify_code/', verify_code, name='verify_code'),

    path('campuses/', CampusListView.as_view(), name='campus-list'), 
    path('campus/<int:campus_id>/', CampusDetailView.as_view(), name='campus-details'), 

    path('buildings/', BuildingListView.as_view(), name='building-list'),

    path('booking/', BookingManagementView.as_view(), name='booking'),
    
    path('building/<int:building_id>/', BuildingDetailstView.as_view(), name='building-details'),
    path('building/<int:building_id>/spaces/', SpacesByBuildingView.as_view(), name='spaces_by_building'),

    path('booking/', BookingManagementView.as_view(), name='booking'),
    path('bookings/', BookingListView.as_view(), name='booking-list'),
    path('booking/<int:booking_id>/', BookingManagementView.as_view(), name='delete-booking'),

    path('find-available-seats/', FindAvailableSeatsView.as_view(), name='find_available_seats'),

    path('find-available-spaces/',find_available_spaces, name='find_available_spaces'),
    path('occupation-actual/<int:space_id>/', occupation_actual, name='occupation-actual'),

    path('get-random-images/', get_random_images, name='get-random-images'),
    
    path('register/', RegisterView.as_view(), name='register'),
    path('enviar_correo/', send_email_view, name='enviar_correo'),
    path('verify_code/', verify_code, name='verify_code'),

    path('invite/', invite, name='invite'),
    path('find_nearby_seats/', find_nearby_seats, name='find_nearby_seats'),
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
