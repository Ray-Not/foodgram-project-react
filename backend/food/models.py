from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from users.models import User

MIN_COOKING_TIME = 1
MAX_COOKING_TIME = 32000
MIN_AMOUNT = 1
MAX_AMOUNT = 1000


class Tag(models.Model):
    """Модель тэгов"""
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name='Название тэга',
    )
    color = models.CharField(
        unique=True,
        max_length=7,
        verbose_name='Цвет тэга в формате HEX',
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Слаг тэга',
    )

    class Meta:
        ordering = ('color', )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Модель Ингредиентов с выбором единиц измерений"""
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=128,
        verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name', )
        unique_together = ('name', 'measurement_unit', )

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipesIngredient',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тэг',
        related_name='tags',
    )
    image = models.ImageField(
        upload_to='food/',
        blank=True,
        null=True,
        verbose_name='Картинка рецепта'
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(MIN_COOKING_TIME),
            MaxValueValidator(MAX_COOKING_TIME)
        ],
        verbose_name='Время готовки (мин.)',
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ('-created_at', )
        unique_together = ('name', )

    def __str__(self):
        return self.name

    def favorite_count(self):
        return Favorite.objects.filter(recipe=self).count()


class RecipesIngredient(models.Model):
    """Связываящая модель Рецепт->Ингредиент"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipe_ingredients'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='recipe_ingredients'
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингредиента',
        validators=[
            MinValueValidator(MIN_AMOUNT),
            MaxValueValidator(MAX_AMOUNT)
        ],
    )

    class Meta:
        ordering = ('recipe', )

    def __str__(self):
        return f'{self.recipe} с использованием {self.ingredient}'


class ShoppingCart(models.Model):
    """Модель для списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_recipes_cart'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    in_shopping_card = models.BooleanField(default=False)

    class Meta:
        ordering = ('user', )
        unique_together = ('user', 'recipe', )

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в список покупок"


class Favorite(models.Model):
    """Модель для избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='user_recipes_favor'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    in_favorite = models.BooleanField(default=False)

    class Meta:
        ordering = ('user', )
        unique_together = ('user', 'recipe', )

    def __str__(self):
        return f"{self.recipe} в избранном у {self.user}"
