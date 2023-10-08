import base64

from django.core.files.base import ContentFile
from rest_framework import serializers

from users.serializers import CustomMeSerializer

from .models import Ingredient, Recipe, RecipesIngredient, Tag


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
    image = Base64ImageField(required=False, allow_null=True)

    def create(self, validated_data):
        """Переопределяем создание с автором"""
        author = self.context['request'].user
        validated_data['author'] = author
        ingredient_data = validated_data.pop('ingredients')
        tags_data = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)

        for item in ingredient_data:
            ingredient = item['id']
            amount = item['amount']
            RecipesIngredient.objects.create(
                ingredient=ingredient,
                recipe=recipe,
                amount=amount
            )

        for tag in tags_data:
            recipe.tags.add(tag)

        return recipe

    def to_representation(self, instance):
        """Переопределим отображение, вернется обычный рецептовый"""
        return RecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

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
