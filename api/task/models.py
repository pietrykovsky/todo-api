from django.db import models

from django.conf import settings

class Task(models.Model):
    """Task model."""
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created']
