from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from unittest.mock import patch, MagicMock

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = MagicMock(spec=User)
        self.user.username = 'testuser'
        self.user.email = 'test@example.com'
        self.user.password = 'testpass123'
        self.user.is_active = True
        
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        self.home_url = reverse('home')

    @patch('django.contrib.auth.models.User.objects')
    def test_login_wrong_password(self, mock_user_objects):
        mock_user_objects.get.return_value = None
        response = self.client.post(self.login_url, {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/login.html')

    @patch('django.contrib.auth.models.User.objects')
    def test_signup_existing_username(self, mock_user_objects):
        mock_user_objects.filter.return_value.exists.return_value = True
        response = self.client.post(self.signup_url, {
            'username': 'testuser',
            'email': 'another@example.com',
            'password1': 'anotherpass123',
            'password2': 'anotherpass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/signup.html')

    @patch('django.contrib.auth.models.User.objects')
    def test_home_page_authenticated(self, mock_user_objects):
        mock_user_objects.get.return_value = self.user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(self.home_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    @patch('django.contrib.auth.models.User.objects')
    def test_logout(self, mock_user_objects):
        mock_user_objects.get.return_value = self.user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get('/logout/')
        self.assertEqual(response.status_code, 302)