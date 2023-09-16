from djoser.serializers import UserSerializer
from rest_framework import serializers

from .models import User


class CustomUserSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    last_name = serializers.CharField(required=True)

    def create(self, validated_data):
        """Создание пользователя с хэш-паролем"""
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def to_representation(self, instance):
        """Переопределение полей в зависимости от метода запроса"""
        data = super().to_representation(instance)
        request = self.context.get('request')
        if request and request.method == 'GET':
            return data
        data.pop('is_subscribed')
        return data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password',
            'is_subscribed',
        )


class CustomMeSerializer(UserSerializer):
    """Переопределение сериализатора Djoser для /me/"""
    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )
