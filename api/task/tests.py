from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Task

def create_task(title='test title', description='test description', user=None):
    """Create and return a task."""
    return Task.objects.create(title=title, description=description, user=user)

def create_user(username='testusername', email='test@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(username=username, email=email, password=password)

class TaskModelTests(TestCase):
    """Test task model."""

    def test_create_task(self):
        """Test create a task objects."""
        user = create_user()
        task = create_task(title='test', description='test dsc', user=user)

        self.assertEqual(task.user, user)
        self.assertEqual(task.title, 'test')
        self.assertEqual(task.description, 'test dsc')
        self.assertFalse(task.is_completed)
