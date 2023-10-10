from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
import csv
from django.http import HttpResponse
from users.serializers import DetailRecipeSerializer
from users.views import ListPagination

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipesIngredient
from .serializers import (CrRecipeSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer)


class TagViewSet(ReadOnlyModelViewSet):
    """Представление вернет список тэгов или тэг"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny, ]


class IngredientViewSet(ReadOnlyModelViewSet):
    """Представление вернет список ингредиентов или ингредиент"""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [AllowAny, ]

    def get_queryset(self):
        """Вернет отфильтрованный запрос по первой фразе"""
        # Регистрозависимо
        queryset = super().get_queryset()
        name_param = self.request.query_params.get('name', '')
        return queryset.filter(name__startswith=name_param)


class RecipeViewSet(ModelViewSet):
    """Представление вернет список рецептов или рецепт"""
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ListPagination
    http_method_names = ['get', 'post', 'delete', 'patch']

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeSerializer
        return CrRecipeSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        response_data = {
            "detail":
                "Permission denied"
        }
        if instance.author != request.user:
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        """Добавление в список покупок"""
        recipe = self.get_object()
        user = request.user
        recipe_in_cart = ShoppingCart.objects.filter(
            user=user,
            recipe=recipe,
            in_shopping_card=True
        )
        if request.method == "POST":
            if recipe_in_cart:
                return Response(
                    {"errors": "recipe_in_cart already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            ShoppingCart.objects.create(
                user=user,
                recipe=recipe,
                in_shopping_card=True
            )
            recipe_serializer = DetailRecipeSerializer(recipe)
            return Response(
                recipe_serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == "DELETE":
            if not recipe_in_cart:
                return Response(
                    {"errors": "recipe_in_cart not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe_in_cart.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST', 'DELETE'], url_path='favorite')
    def favorite(self, request, pk=None):
        """Добавление в избранное"""
        recipe = self.get_object()
        user = request.user
        recipe_in_favor = Favorite.objects.filter(
            user=user,
            recipe=recipe,
            in_favorite=True
        )
        if request.method == "POST":
            if recipe_in_favor:
                return Response(
                    {"errors": "recipe_in_favore already exists"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            Favorite.objects.create(
                user=user,
                recipe=recipe,
                in_favorite=True
            )
            recipe_serializer = DetailRecipeSerializer(recipe)
            return Response(
                recipe_serializer.data,
                status=status.HTTP_201_CREATED
            )
        if request.method == "DELETE":
            if not recipe_in_favor:
                return Response(
                    {"errors": "recipe_in_favore not found"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            recipe_in_favor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@login_required
def dowload_shopping_list(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="shop_list.csv"'
    writer = csv.writer(response, delimiter=',')
    ingredient_totals = {}
    ingredient_units = {}
    shopping_cart_items = ShoppingCart.objects.filter(user=request.user)
    for item in shopping_cart_items:
        recipe_ingredients = RecipesIngredient.objects.filter(
            recipe=item.recipe
        )
        for recipe_ingredient in recipe_ingredients:
            ingredient_name = recipe_ingredient.ingredient.name
            measure = recipe_ingredient.ingredient.measurement_unit
            if ingredient_name in ingredient_totals:
                ingredient_totals[ingredient_name] += recipe_ingredient.amount
            else:
                ingredient_totals[ingredient_name] = recipe_ingredient.amount
                ingredient_units[ingredient_name] = measure
    for ingredient, amount in ingredient_totals.items():
        measure = ingredient_units[ingredient]
        formatted_view = f'{ingredient} ({measure}) - {amount}'
        writer.writerow([formatted_view])

    return response
