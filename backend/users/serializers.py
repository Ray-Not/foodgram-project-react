from .models import User
from djoser.serializers import UserSerializer


class CustomRegisterSerializer(UserSerializer):
    """Кастомный сериализатор для джосера"""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed'
        )
