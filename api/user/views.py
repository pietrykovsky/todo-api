from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth import get_user_model

from drf_spectacular.utils import extend_schema

from .serializers import UserSerializer

@extend_schema(
    request = UserSerializer,
    responses = UserSerializer
)
@api_view(['POST'])
def create_user_view(request):
    """Create a new user view."""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)