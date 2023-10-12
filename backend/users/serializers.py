from djoser.serializers import UserSerializer
from rest_framework import serializers

from food.models import Recipe

from .models import Subscribe, User


class DetailRecipeSerializer(serializers.ModelSerializer):
    """Сокращенный сериализатор рецепта"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class CustomUserSerializer(serializers.ModelSerializer):
    """Кастомный сериализатор для создания пользователя"""
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    last_name = serializers.CharField(required=True)
    is_subscribed = serializers.SerializerMethodField()

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

    def get_is_subscribed(self, follow):
        """Для определения is_subscribe"""
        follower = self.context['request'].user
        if follower.is_anonymous:
            return False
        return Subscribe.objects.filter(
            follow=follow,
            follower=follower
        ).exists()

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


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    def get_recipes(self, follow):
        """Возвращение рецептов фолоува"""
        recipes = Recipe.objects.filter(author=follow)
        serializer = DetailRecipeSerializer(recipes, many=True)

        return serializer.data

    def get_recipes_count(self, follow):
        """Вернет количество рецептов после recipes"""
        return Recipe.objects.filter(author=follow).count()

    def get_is_subscribed(self, follow):
        """Для работы is_subscribed"""
        follower = self.context['request'].user
        return Subscribe.objects.filter(
            follow=follow,
            follower=follower
        ).exists()

    def to_representation(self, instance):
        """Для ограничения вложенных рецептов"""
        data = super().to_representation(instance)
        recipes_limit = self.context.get('recipes_limit')
        print(recipes_limit)
        if recipes_limit is not None:
            data['recipes'] = data['recipes'][:recipes_limit]
            data['recipes_count'] = recipes_limit
        return data

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
