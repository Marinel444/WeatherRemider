from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


class WeatherAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return {'refresh': str(refresh), 'access': str(refresh.access_token)}

    def test_protected_endpoint_with_jwt(self):
        tokens = self.get_tokens_for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {tokens["access"]}')

        response = self.client.get('http://127.0.0.1:8000/api/v1/city/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response2 = self.client.get('http://127.0.0.1:8000/api/v1/weather/')
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        response3 = self.client.get('http://127.0.0.1:8000/api/v1/subscribe/')
        self.assertEqual(response3.status_code, status.HTTP_200_OK)
