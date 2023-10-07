from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from .models import Tag, Ingredient, Recipe
from .serializers import TagSerializer, IngredientSerializer, RecipeSerializer
from users.views import ListPagination


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
        queryset = super().get_queryset()
        name_param = self.request.query_params.get('name', '')
        return queryset.filter(name__startswith=name_param)


class RecipeViewSet(ModelViewSet):
    """Представление вернет список рецептов или рецепт"""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, ]
    pagination_class = ListPagination
