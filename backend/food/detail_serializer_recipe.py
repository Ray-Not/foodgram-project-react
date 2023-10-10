from .models import Recipe
from rest_framework import serializers


class DetailRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода при добавлении в корзину"""
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
