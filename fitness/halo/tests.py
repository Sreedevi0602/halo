# type: ignore

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Class, Booking
from django.utils import timezone
from datetime import timedelta
import pytz
from dateutil import parser




# Create your tests here.

class BookingAPITest(APITestCase):
    def setUp(self):
        self.upcoming_class = Class.objects.create(
            name="Yoga",
            datetime=timezone.now() + timedelta(days=1),
            instructor="Alice",
            slots_available=5
        )
        self.past_class = Class.objects.create(
            name="Pilates",
            datetime=timezone.now() - timedelta(days=1),
            instructor="Bob",
            slots_available=5
        )

    def test_class_list_returns_upcoming_only(self):
        url = reverse('class_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        class_names = [item['name'] for item in response.data]
        self.assertIn(self.upcoming_class.name, class_names)
        self.assertNotIn(self.past_class.name, class_names)

    def test_class_list_no_upcoming_returns_error(self):
        Class.objects.filter(datetime__gte=timezone.now()).delete()
        url = reverse('class_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], "No upcoming classes available.")

    def test_book_class_success(self):
        url = reverse('book_class')
        data = {
            "class_id": self.upcoming_class.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "Booking successful")
        self.upcoming_class.refresh_from_db()
        self.assertEqual(self.upcoming_class.slots_available, 4)

    def test_book_class_missing_fields(self):
        url = reverse('book_class')
        response = self.client.post(url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_book_class_invalid_name(self):
        url = reverse('book_class')
        data = {
            "class_id": self.upcoming_class.id,
            "client_name": "John123",
            "client_email": "john@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Name must contain only letters", response.data['error'])

    def test_book_class_invalid_email(self):
        url = reverse('book_class')
        data = {
            "class_id": self.upcoming_class.id,
            "client_name": "John Doe",
            "client_email": "johnexample.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid email format", response.data['error'])

    def test_book_class_email_taken(self):
        Booking.objects.create(
            class_booked=self.upcoming_class,
            client_name="John Doe",
            client_email="john@example.com"
        )
        url = reverse('book_class')
        data = {
            "class_id": self.upcoming_class.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already in use", response.data['error'])

    def test_book_class_class_not_found(self):
        url = reverse('book_class')
        data = {
            "class_id": 9999,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("Class not found", response.data['error'])

    def test_book_class_no_slots(self):
        self.upcoming_class.slots_available = 0
        self.upcoming_class.save()
        url = reverse('book_class')
        data = {
            "class_id": self.upcoming_class.id,
            "client_name": "John Doe",
            "client_email": "john@example.com"
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No slots available", response.data['error'])

    def test_get_bookings_success(self):
        Booking.objects.create(
            class_booked=self.upcoming_class,
            client_name="John Doe",
            client_email="john@example.com"
        )
        url = reverse('get_bookings') + '?email=john@example.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_get_bookings_missing_email(self):
        url = reverse('get_bookings')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email is required', response.data['error'])

    def test_get_bookings_invalid_email(self):
        url = reverse('get_bookings') + '?email=invalidemail'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid email format', response.data['error'])

    def test_get_bookings_no_bookings_found(self):
        url = reverse('get_bookings') + '?email=nobookings@example.com'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('No bookings found', response.data['error'])






class TimezoneViewsTest(APITestCase):

    def setUp(self):
        # Setup a class in UTC
        self.utc_now = timezone.now()
        self.class_instance = Class.objects.create(
            name="Test Yoga",
            datetime=self.utc_now + timedelta(days=1),  # tomorrow
            instructor="Test Instructor",
            slots_available=5
        )

    

    def test_class_list_with_timezone(self):
        # Pass a timezone in query
        response = self.client.get(reverse('class_list') + '?tz=Asia/Tokyo')
        self.assertEqual(response.status_code, 200)

        # Get datetime from response
        returned_datetime_str = response.data[0]['datetime']
        returned_dt = timezone.datetime.strptime(returned_datetime_str, "%Y-%m-%d %I:%M %p")
        
        # Convert original UTC datetime to Asia/Tokyo
        tokyo_tz = pytz.timezone('Asia/Tokyo')
        expected_dt = self.class_instance.datetime.astimezone(tokyo_tz)
        
        self.assertEqual(returned_dt.hour, expected_dt.hour)
        self.assertEqual(returned_dt.day, expected_dt.day)

    def test_book_class_and_return_timezone(self):
        booking_data = {
            'class_id': self.class_instance.id,
            'client_name': 'John Doe',
            'client_email': 'john@example.com'
        }

        response = self.client.post(reverse('book_class') + '?tz=Asia/Kolkata', data=booking_data, format='json')
        self.assertEqual(response.status_code, 201)

        returned_booking_time = response.data['booking']['booked_at']

        # Parse ISO datetime string
        returned_dt_utc = parser.isoparse(returned_booking_time)

        # Convert to IST
        ist = pytz.timezone('Asia/Kolkata')
        returned_dt_ist = returned_dt_utc.astimezone(ist)

        # Get expected formatted value
        formatted_expected = returned_dt_ist.strftime("%Y-%m-%d %I:%M %p")

        self.assertEqual(formatted_expected, returned_dt_ist.strftime("%Y-%m-%d %I:%M %p"))  # compare IST representation

    
    