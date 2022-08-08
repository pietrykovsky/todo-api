from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient, force_authenticate

from .models import Task
from .serializers import TaskSerializer

TASKS_URL = reverse('task:task-list')

def detail_task(task_id):
    """Create and return a task detail url."""
    return reverse('task:task-detail', args=[task_id])

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

class PublicTaskApiTests(TestCase):
    """Test public task api."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_task_list_without_auth(self):
        """Test retrieve task list without being authenticated throws an error."""
        response = self.client.get(TASKS_URL)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_task_without_auth(self):
        """Test create a task without being logged in throws an error."""
        user = create_user()
        payload = {
            'title': 'test title',
            'description': 'test description',
            'user': user,
        }
        response = self.client.post(TASKS_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        exists = Task.objects.filter(title=payload['title']).exists()
        self.assertFalse(exists)

class PrivateTaskApiTests(TestCase):
    """Test private task api."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_task_list_success(self):
        """Test retrieve tasks is successful."""
        create_task('test1', user=self.user)
        create_task('test2', user=self.user)
        response = self.client.get(TASKS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_task_list_limited_to_user(self):
        """Test task list is limited to owner."""
        other_user = create_user(username='anotheruser', email='another@example.com')
        create_task(title='test1', user=other_user)
        task = create_task(title='test2', user=self.user)
        response = self.client.get(TASKS_URL)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = TaskSerializer(task)
        self.assertEqual(response.data, serializer.data)