import django_filters
from django.db.models import Q

from .models import Favorite, Ingredient, Recipe, ShoppingCart


class RecipeFilter(django_filters.FilterSet):
    """Фильтры для рецептов"""
    is_favorited = django_filters.NumberFilter(
        method='filter_in_favorite'
    )
    is_in_shopping_cart = django_filters.NumberFilter(
        method='filter_in_shop_list'
    )
    author = django_filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = django_filters.CharFilter(
        method='filter_tags'
    )

    def filter_in_favorite(self, queryset, name, value):
        """Фильтр для избранного"""
        user = self.request.user
        if user.is_anonymous:
            return queryset
        is_favorited = bool(value)
        favorites = Favorite.objects.filter(user=user)
        favorite_recipes = [favorite.recipe for favorite in favorites]
        if is_favorited:
            return queryset.filter(
                pk__in=[recipe.pk for recipe in favorite_recipes]
            )
        else:
            return queryset.exclude(
                pk__in=[recipe.pk for recipe in favorite_recipes]
            )

    def filter_in_shop_list(self, queryset, name, value):
        """Фильтр для списка покупок"""
        user = self.request.user
        if user.is_anonymous:
            return queryset
        is_in_shopping_list = bool(value)
        shop_list = ShoppingCart.objects.filter(user=user)
        added_recipes = [shop_item.recipe for shop_item in shop_list]
        if is_in_shopping_list:
            return queryset.filter(
                pk__in=[recipe.pk for recipe in added_recipes]
            )
        else:
            return queryset.exclude(
                pk__in=[recipe.pk for recipe in added_recipes]
            )

    def filter_tags(self, queryset, name, value):
        """Фильтр для тэгов"""
        tags = self.request.GET.getlist('tags')
        tag_filters = Q()
        for tag in tags:
            tag_filters |= Q(tags__slug=tag)
        return queryset.filter(tag_filters).distinct()

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        )


class IngredientFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
