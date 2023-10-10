from django.contrib import admin

from .models import Ingredient, Recipe, RecipesIngredient, ShoppingCart, Tag


class RecipeAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    pass


class TagAdmin(admin.ModelAdmin):
    pass


admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Tag)
admin.site.register(RecipesIngredient)
admin.site.register(ShoppingCart)
