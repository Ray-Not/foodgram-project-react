import django_filters

from .models import Favorite, Recipe, ShoppingCart


class RecipeFilter(django_filters.FilterSet):
    """Фильтры для рецептов"""
    is_favorited = django_filters.BooleanFilter(
        method='filter_in_favorite'
    )
    is_in_shopping_cart = django_filters.BooleanFilter(
        method='filter_in_shop_list'
    )
    author = django_filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = django_filters.CharFilter(
        field_name='tags__slug',
        lookup_expr='exact'
    )

    def filter_in_favorite(self, queryset, name, value):
        """Фильтр для избранного"""
        user = self.request.user
        if user.is_anonymous:
            return queryset
        favorites = Favorite.objects.filter(user=user)
        favorite_recipes = [favorite.recipe for favorite in favorites]
        if value:
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
        shop_list = ShoppingCart.objects.filter(user=user)
        added_recipes = [shop_item.recipe for shop_item in shop_list]
        if value:
            return queryset.filter(
                pk__in=[recipe.pk for recipe in added_recipes]
            )
        else:
            return queryset.exclude(
                pk__in=[recipe.pk for recipe in added_recipes]
            )

    class Meta:
        model = Recipe
        fields = (
            'tags',
            'author',
            'is_favorited',
            'is_in_shopping_cart'
        )
