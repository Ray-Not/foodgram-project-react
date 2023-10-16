import base64

from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from users.serializers import CustomMeSerializer

from .models import (MAX_AMOUNT, MAX_COOKING_TIME, MIN_AMOUNT,
                     MIN_COOKING_TIME, Ingredient, Recipe, RecipesIngredient,
                     Tag)


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
    amount = serializers.IntegerField(
        min_value=MIN_AMOUNT,
        max_value=MAX_AMOUNT
    )

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
    cooking_time = serializers.IntegerField(
        min_value=MIN_COOKING_TIME,
        max_value=MAX_COOKING_TIME
    )

    def get_is_in_shopping_cart(self, obj):
        """Для отображения поля в списке покупок"""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        is_in_cart = user.user_recipes_cart.filter(recipe=obj).exists()

        return is_in_cart

    def get_is_favorited(self, obj):
        """Для отображения поля в избранном"""
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        is_in_cart = user.user_recipes_favor.filter(recipe=obj).exists()

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
    ingredients = CrRecipeIngredientSerializer(many=True, required=True)
    image = Base64ImageField(required=True, allow_null=True)

    def create(self, validated_data):
        """POST для рецепта"""
        author = self.context['request'].user
        validated_data['author'] = author
        ingredient_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe_ingredients_objects = []
        get_recipe_ingredient_objects(
            ingredient_data,
            recipe,
            recipe_ingredients_objects
        )
        RecipesIngredient.objects.bulk_create(recipe_ingredients_objects)
        for tag in tags_data:
            recipe.tags.add(tag)
        return recipe

    def update(self, instance, validated_data):
        """PATCH для рецепта"""
        if instance.author != self.context['request'].user:
            raise PermissionDenied
        instance.name = validated_data.get('name')
        instance.cooking_time = validated_data.get('cooking_time')
        instance.text = validated_data.get('text')
        validated_data.get('image', instance.image)
        instance.tags.set(validated_data.get('tags'))
        instance.ingredients.clear()
        recipe_ingredients_objects = []
        get_recipe_ingredient_objects(
            validated_data.get('ingredients'),
            instance,
            recipe_ingredients_objects
        )
        RecipesIngredient.objects.bulk_create(recipe_ingredients_objects)
        instance.save()
        return instance

    def to_representation(self, instance):
        """Переопределим отображение, вернется обычный рецептовый"""
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

    def validate_ingredients(self, data):
        seen_ids = set()
        for item in data:
            ingredient_id = item.get('id')
            if ingredient_id in seen_ids:
                raise serializers.ValidationError("Duplicated ingredient id")
            seen_ids.add(ingredient_id)
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


def get_recipe_ingredient_objects(ingredient_data,
                                  recipe,
                                  recipe_ingredients_objects):

    for item in ingredient_data:
        ingredient = item['id']
        amount = item['amount']
        recipe_ingredient = RecipesIngredient(
            recipe=recipe,
            ingredient=ingredient,
            amount=amount
        )
        recipe_ingredients_objects.append(recipe_ingredient)

    return recipe_ingredients_objects
