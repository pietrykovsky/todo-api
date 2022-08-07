from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager

class UserManager(BaseUserManager):
    """Manager for users."""
    def create_user(self, username, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Please provide an email address.')
        
        return BaseUserManager.create_user(self, username, email, password, **extra_fields)

class User(AbstractUser):
    """User model."""
    email = models.EmailField(unique=True)

    objects = UserManager()
