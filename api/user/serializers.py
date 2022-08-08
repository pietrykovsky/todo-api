from rest_framework import serializers

from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user model."""

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True, 
                'min_length': 8,
            }
        }

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return a user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user