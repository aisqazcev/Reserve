from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Building, Campus, CustomUser
from django.contrib.auth.hashers import check_password

class UserCreationTests(APITestCase):
    def test_create_user_success(self):
        url = reverse('reserve:register')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'name': 'Test User',
            'password': 'testpassword123'
        }
        response = self.client.post(url, data, format='json')
        
        # Verificar la respuesta de la API
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response.data)
        
        # Verificar la creación en la base de datos
        self.assertEqual(CustomUser.objects.count(), 1)
        user = CustomUser.objects.get()
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.username, 'newuser')
        
        # Verificar la encriptación de la contraseña
        self.assertTrue(check_password('testpassword123', user.password))

class BuildingDetailViewTests(APITestCase):
    def setUp(self):
        self.campus = Campus.objects.create(campus_name="Main Campus")
        self.building = Building.objects.create(
            name="Main Building",
            name_complete="Main Academic Building",
            address="123 College St",
            web="http://www.university.edu/main",
            email="main@university.edu",
            phone="123-456-7890",
            services="General academic services",
            campus=self.campus
        )
        self.url = reverse('reserve:building-details', kwargs={'building_id': self.building.id})

    def test_get_building_details(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.building.name)

    def test_get_building_details_not_found(self):
        url = reverse('reserve:building-details', kwargs={'building_id': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
