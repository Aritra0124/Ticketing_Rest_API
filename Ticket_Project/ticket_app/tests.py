import json
from django.test import TestCase
from .models import Manager, Location, Pricing, Ticket, Travellers
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.hashers import check_password

class TicketModelTestCase(TestCase):
    def setUp(self):
        self.location1 = Location.objects.create(name='Location 1')
        self.location2 = Location.objects.create(name='Location 2')
        self.manager = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.pricing = Pricing.objects.create(source=self.location1, destination=self.location2, pricing=50.00)
        self.ticket = Ticket.objects.create(
            source=self.location1,
            destination=self.location2,
            travel_date='2023-10-10',
            passenger_name='Test Passenger',
            pricing=self.pricing,
            seat_number='A1'
        )

    def test_ticket_creation(self):
        ticket = Ticket.objects.get(id=1)
        self.assertEqual(ticket.source, self.location1)
        self.assertEqual(ticket.destination, self.location2)
        self.assertEqual(ticket.passenger_name, 'Test Passenger')
        self.assertEqual(ticket.pricing, self.pricing)
        self.assertEqual(ticket.seat_number, 'A1')
        self.assertFalse(ticket.is_cancelled)

    def test_traveller_creation(self):
        traveller = Travellers.objects.create(ticket=self.ticket)
        self.assertEqual(traveller.ticket, self.ticket)

    def test_location_str_representation(self):
        self.assertEqual(str(self.location1), 'Location 1')

    def test_pricing_str_representation(self):
        pricing = Pricing.objects.get(id=1)
        expected_str = f'Pricing from {self.location1.name} to {self.location2.name}: 50.00'
        self.assertEqual(str(pricing), expected_str)

    def test_manager_creation(self):
        manager = Manager.objects.create_user(username='testmanager', password='testpassword')
        self.assertEqual(manager.username, 'testmanager')




class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.manager_data = {
            "username": "admin@admin",
            "password": "Hello@1234"
        }
        self.client.post('/api/register/', self.manager_data, format='json')

    # def test_manager_registration(self):
    #     data = {
    #         "username": "admin@admin",
    #         "password": "Hello@1234"
    #     }
    #     response = self.client.post('/api/register/', data)
    #     print(response.content)
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_manager_login(self):
        data = {
            "username": "admin@admin",
            "password": "Hello@1234"
        }

        response = self.client.post('/api/login/', data)
        print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user = Manager.objects.get(username=data['username'])
        self.assertTrue(check_password(data['password'], user.password))

    # def test_ticket_creation(self):
    #     # Test Ticket Creation API endpoint
    #     data = {
    #         # Provide necessary data for creating a ticket
    #     }
    #     response = self.client.post('/api/ticket/', data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     # Assert other ticket creation-related behaviors as needed
    #
    # # Write similar test methods for other API endpoints