from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from users.views import ListPagination
from rest_framework.response import Response
from rest_framework import status

from .models import Ingredient, Recipe, Tag
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
        response_data = {"detail": "У вас недостаточно прав для выполнения данного действия."}
        if instance.author != request.user:
            return Response(response_data, status=status.HTTP_403_FORBIDDEN)

    @action(detail=True, methods=['POST'], url_path='shopping_cart')
    def shopping_cart(self, request, pk=None):
        return Response({"detail": "Запрос на добавление в корзину успешно обработан."})
