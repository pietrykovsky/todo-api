from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from .serializers import TaskDetailSerializer, TaskSerializer
from .models import Task
class TaskViewSet(viewsets.ModelViewSet):
    """View for managing task api."""
    serializer_class = TaskDetailSerializer
    queryset = Task.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Get the list of items for this view."""
        queryset = Task.objects.filter(user=self.request.user)
        return queryset

    def perform_create(self, serializer):
        """Create a new task."""
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        """Return the serializer class for request."""
        if self.action == 'list':
            return TaskSerializer
        return self.serializer_class