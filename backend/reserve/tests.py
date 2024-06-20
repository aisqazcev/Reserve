from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser, Equipment, Campus, Building, Space, Desk, Booking
from django.utils import timezone
from datetime import datetime, timedelta

class CustomUserTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', name='Test User', email='testuser@example.com', password='password123')
    
    def test_create_user(self):
        user = CustomUser.objects.get(username='testuser')
        self.assertEqual(user.email, 'testuser@example.com')

    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser@example.com')
        
    def test_change_password(self):
        self.user.set_password('new_password123')
        self.user.save()
        self.assertTrue(self.user.check_password('new_password123'))

class EquipmentTests(TestCase):
    def setUp(self):
        self.equipment = Equipment.objects.create(name='Projector')

    def test_create_equipment(self):
        equipment = Equipment.objects.get(name='Projector')
        self.assertEqual(equipment.name, 'Projector')

    def test_equipment_str(self):
        self.assertEqual(str(self.equipment), 'Projector')

class CampusTests(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(campus_name='Main Campus')

    def test_create_campus(self):
        campus = Campus.objects.get(campus_name='Main Campus')
        self.assertEqual(campus.campus_name, 'Main Campus')

    def test_campus_str(self):
        self.assertEqual(str(self.campus), 'Main Campus')

class BuildingTests(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(campus_name='Main Campus')
        self.building = Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=self.campus)

    def test_create_building(self):
        building = Building.objects.get(name='Main Building')
        self.assertEqual(building.name, 'Main Building')

    def test_building_str(self):
        self.assertEqual(str(self.building), 'Main Building')

class SpaceTests(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(campus_name='Main Campus')
        self.building = Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=self.campus)
        self.space = Space.objects.create(name='Main Space', building=self.building, capacity=100, general_info='General Info', schedule='9-5')

    def test_create_space(self):
        space = Space.objects.get(name='Main Space')
        self.assertEqual(space.name, 'Main Space')

    def test_space_str(self):
        self.assertEqual(str(self.space.name), 'Main Space')

class DeskTests(TestCase):
    def setUp(self):
        self.campus = Campus.objects.create(campus_name='Main Campus')
        self.building = Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=self.campus)
        self.space = Space.objects.create(name='Main Space', building=self.building, capacity=100, general_info='General Info', schedule='9-5')
        self.desk = Desk.objects.create(name='Main Desk', space_id=self.space, seat_status=0)

    def test_create_desk(self):
        desk = Desk.objects.get(name='Main Desk')
        self.assertEqual(desk.name, 'Main Desk')

    def test_desk_nearby(self):
        nearby_desk = Desk.objects.create(name='Nearby Desk', space_id=self.space, seat_status=0)
        self.desk.nearby_pl.add(nearby_desk)
        self.assertIn(nearby_desk, self.desk.nearby_pl.all())

class BookingTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', name='Test User', email='testuser@example.com', password='password123')
        self.campus = Campus.objects.create(campus_name='Main Campus')
        self.building = Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=self.campus)
        self.space = Space.objects.create(name='Main Space', building=self.building, capacity=100, general_info='General Info', schedule='9-5')
        self.desk = Desk.objects.create(name='Main Desk', space_id=self.space, seat_status=0)
        self.booking = Booking.objects.create(user=self.user, campus=self.campus, building=self.building, space=self.space, desk=self.desk, date=datetime.today(), start_time=timezone.now(), duration=timedelta(hours=1), end_time=timezone.now() + timedelta(hours=1))

    def test_create_booking(self):
        booking = Booking.objects.get(user=self.user)
        self.assertEqual(booking.user, self.user)

class ApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = CustomUser.objects.create_user(username='testuser', name='Test User', email='testuser@example.com', password='password123')
        self.client.force_authenticate(user=self.user)

    def test_login(self):
        response = self.client.post(reverse('reserve:login'), {'username_or_email': 'testuser@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_register(self):
        response = self.client.post(reverse('reserve:register'), {'username': 'newuser', 'name': 'New User', 'email': 'newuser@example.com', 'password': 'password123'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_campuses(self):
        Campus.objects.create(campus_name='Main Campus')
        response = self.client.get(reverse('reserve:campus-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_get_buildings(self):
        campus = Campus.objects.create(campus_name='Main Campus')
        Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=campus)
        response = self.client.get(reverse('reserve:building-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_get_spaces(self):
        campus = Campus.objects.create(campus_name='Main Campus')
        building = Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=campus)
        Space.objects.create(name='Main Space', building=building, capacity=100, general_info='General Info', schedule='9-5')
        response = self.client.get(reverse('reserve:spaces_by_building', kwargs={'building_id': building.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_booking(self):
        campus = Campus.objects.create(campus_name='Main Campus')
        building = Building.objects.create(name='Main Building', name_complete='Main Building Complete', address='123 Main St', web='http://example.com', email='building@example.com', phone='123456789', services='WiFi', campus=campus)
        space = Space.objects.create(name='Main Space', building=building, capacity=100, general_info='General Info', schedule='9-5')
        desk = Desk.objects.create(name='Main Desk', space_id=space, seat_status=0)
        response = self.client.post(reverse('reserve:booking'), {
            'desk': desk.id,
            'start_time': (timezone.now() + timedelta(hours=1)).isoformat(),
            'duration': 60
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
