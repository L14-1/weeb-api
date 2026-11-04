from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Profile, Role


User = get_user_model()

class AuthTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user@test.com',
            email='user@test.com',
            password='test1234!',
            first_name='Jean',
            last_name='Test',
            is_active=True,
        )

        Profile.objects.create(
            user=self.user,
            role=Role.MEMBER
        )


    def test_register_create_unactive_user(self):
        url = reverse('signup')

        data = {
            'first_name': 'Test',
            'last_name': 'Test',
            'email': 'basile@test.com',
            'password': 'test1234!',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = User.objects.get(email='basile@test.com')
        self.assertFalse(user.is_active)
        self.assertEqual(user.profile.role, Role.MEMBER)


    def test_login_return_tokens(self):
        url = reverse('login')

        data = {
            'username': 'user@test.com',
            'password': 'test1234!',
        }

        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)


    def test_me_return_auth_user(self):
        url = reverse('me')

        self.client.force_authenticate(user=self.user)

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user@test.com')
        self.assertEqual(response.data['role'], Role.MEMBER)


    # TODO: reset password TU