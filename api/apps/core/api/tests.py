from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apps.core.models import PersonRegistrationRequest


class PersonRegistrationRequestTests(APITestCase):
    def test_create_request(self):
        url = reverse("core_api:registration-requests_create")

        data = {
            "email": "cybersturmer@ya.ru",
            "prefix_url": "pmdragon"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PersonRegistrationRequest.objects.count(), 1)
        self.assertEqual(PersonRegistrationRequest.objects.get().email, data['email'])
        self.assertEqual(PersonRegistrationRequest.objects.get().prefix_url, data['prefix_url'])
