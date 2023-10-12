import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.serializers import CustomMeSerializer

from .models import (Favorite, Ingredient, Recipe, RecipesIngredient,
                     ShoppingCart, Tag)


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тэгов"""
    class Meta:
        model = Tag
        fields = (
            'id',
            'name',
            'color',
            'slug',
        )


class IngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов"""
    class Meta:
        model = Ingredient
        fields = (
            'id',
            'name',
            'measurement_unit',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов->рецептов (просмотр)"""
    id = serializers.ReadOnlyField(
        source='ingredient.id'
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipesIngredient
        fields = (
            'id',
            'name',
            'measurement_unit',
            'amount',
        )


class Base64ImageField(serializers.ImageField):
    """Конвертация из base64"""
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)
        return super().to_internal_value(data)


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для получения рецептов"""
    ingredients = RecipeIngredientSerializer(
        many=True,
        source='recipe_ingredients'
    )
    image = Base64ImageField(required=False, allow_null=True)
    author = CustomMeSerializer()
    tags = TagSerializer(many=True)
    is_in_shopping_cart = serializers.SerializerMethodField()
    is_favorited = serializers.SerializerMethodField()

    def get_is_in_shopping_cart(self, obj):
        """Для отображения поля в списке покупок"""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        is_in_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=obj,
            in_shopping_card=True
        ).exists()

        return is_in_cart

    def get_is_favorited(self, obj):
        """Для отображения поля в избранном"""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        is_in_cart = Favorite.objects.filter(
            user=user,
            recipe=obj,
            in_favorite=True
        ).exists()

        return is_in_cart

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )


class CrRecipeIngredientSerializer(serializers.ModelSerializer):
    """Сериализатор для ингредиентов->рецептов (создание)"""
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipesIngredient
        fields = (
            'id',
            'amount'
        )


class CrRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для создания рецептов"""
    ingredients = CrRecipeIngredientSerializer(many=True)
    image = Base64ImageField(required=True, allow_null=True)

    def create(self, validated_data):
        """POST для рецепта"""
        author = self.context['request'].user
        validated_data['author'] = author
        ingredient_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        for item in ingredient_data:
            ingredient = item['id']
            amount = item['amount']
            recipe_ingredient = RecipesIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient,
                amount=amount
            )
            recipe_ingredient.amount = amount
            recipe_ingredient.save()
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        """PATCH для рецепта"""
        if instance.author != self.context['request'].user:
            raise PermissionDenied
        instance.name = validated_data['name']
        instance.cooking_time = validated_data['cooking_time']
        instance.text = validated_data['text']
        new_image = validated_data.get('image')
        if new_image:
            instance.image = new_image
        instance.tags.set(validated_data.pop('tags'))
        instance.ingredients.clear()
        for item in validated_data['ingredients']:
            ingredient = item['id']
            amount = item['amount']
            RecipesIngredient.objects.create(
                ingredient=ingredient,
                recipe=instance,
                amount=amount
            )
        instance.save()
        return instance

    def to_representation(self, instance):
        """Переопределим отображение, вернется обычный рецептовый"""
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

    def validate(self, data):
        """Валидация, в основном для PATCH"""
        errors = {}
        required_fields = [
            'name',
            'cooking_time',
            'text',
            'ingredients',
            'tags'
        ]
        for field in required_fields:
            if not data.get(field):
                errors[field] = 'This field is required'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def validate_ingredients(self, data):
        """Валидация наличия полей в ingredients и проверка значения amount."""
        errors = []
        for item in data:
            item_errors = {}
            if 'id' not in item:
                item_errors['id'] = 'This field is required'
            if 'amount' not in item:
                item_errors['amount'] = 'This field is required'
            if 'amount' in item and int(item['amount']) < 1:
                item_errors[
                    'amount'
                ] = 'Ensure this value is greater than or equal to 1'
            errors.append(item_errors)
        is_empty_dicts = all(
            isinstance(item, dict) and not item for item in errors
        )
        if not is_empty_dicts:
            raise serializers.ValidationError(errors)
        return data

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
