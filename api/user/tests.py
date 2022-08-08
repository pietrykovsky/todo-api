from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, force_authenticate

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(username='testusername', email='test@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(username=username, email=email, password=password)

class UserModelTests(TestCase):
    """Test user model."""

    def test_create_user(self):
        """Test creating a new user."""
        username='testusername'
        email='test@example.com'
        password='testpass123'
        user = create_user(username, email, password)

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_user_without_email_raises_error(self):
        """Test create user with a blank email raises an error."""
        with self.assertRaises(ValueError):
            create_user(email='')

class PublicUserApiTests(TestCase):
    """Test public user api."""

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """Test create user is successful."""
        payload = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'testpassword123',
        }

        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(username=payload['username'])
        self.assertEqual(user.username, payload['username'])
        self.assertEqual(user.email, payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', response.data)

    def test_create_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'testpassword123',
        }
        create_user(username='testusername123')
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_create_user_with_username_exists_error(self):
        """Test error returned if user with username exists."""
        payload = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'testpassword123',
        }
        create_user(email='test123@example.com')
        response = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is return if password is less than 8 characters."""
        payload = {
            'username': 'testusername',
            'email': 'test@example.com',
            'password': 'test',
        }
        response = self.client.post(CREATE_USER_URL, payload)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(username=payload['username']).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test generate token for valid credentials."""
        payload = {
            'username': 'testusername',
            'password': 'testpass123',
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_bad_credentials(self):
        """Test return error if bad credentials provided."""
        payload = {
            'username': 'testusername',
            'password': 'wrongpassword',
        }
        create_user(payload['username'])
        response = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_blank_password(self):
        """Test return error if no password provided."""
        payload = {
            'username': 'testusername',
            'password': ''
        }
        create_user(**payload)
        response = self.client.post(TOKEN_URL,  payload)

        self.assertNotIn('token', response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)