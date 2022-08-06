from django.test import TestCase
from django.contrib.auth import get_user_model

def create_user(username='testusername', email='test@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(username=username, email=email, password=password)

class UserModelTest(TestCase):
    """Test user model."""

    def test_create_user(self):
        """Test creating a new user."""
        username='testuser'
        email='test@example.com'
        password='testpass123'
        user = create_user()

        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))