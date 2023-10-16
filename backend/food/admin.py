from django.contrib import admin

from .models import (Favorite, Ingredient, Recipe, RecipesIngredient,
                     ShoppingCart, Tag)


class RecipeIngredientInline(admin.TabularInline):
    model = RecipesIngredient
    min_num = 1


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorite_count', 'created_at')
    list_filter = ('name', 'author', 'tags', )
    inlines = (RecipeIngredientInline, )


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit', )
    list_filter = ('name', )


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag)
admin.site.register(RecipesIngredient)
admin.site.register(ShoppingCart)
admin.site.register(Favorite)
