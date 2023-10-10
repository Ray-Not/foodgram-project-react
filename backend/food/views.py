from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from users.serializers import DetailRecipeSerializer
from users.views import ListPagination

from .models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
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
        """Добавление в список покупок"""
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
