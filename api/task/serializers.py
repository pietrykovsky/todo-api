from rest_framework import serializers

from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """Serializer for the task model."""

    class Meta:
        model = Task
        fields = ['id', 'title','is_completed']
        read_only_fields = ['id']