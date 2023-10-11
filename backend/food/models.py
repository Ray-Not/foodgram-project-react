from django.core.validators import MinValueValidator
from django.db import models
from users.models import User


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

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'measurement_unit')


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
    cooking_time = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
        verbose_name='Время готовки (мин.)',
    )
    is_favorited = models.BooleanField(default=False)
    is_in_shopping_cart = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', )


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
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
        blank=False
    )

    def __str__(self):
        return f'{self.recipe} с использованием {self.ingredient}'


class ShoppingCart(models.Model):
    """Модель для списка покупок"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    in_shopping_card = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} добавил {self.recipe} в список покупок"


class Favorite(models.Model):
    """Модель для избранного"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    in_favorite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.recipe} в избранном у {self.user}"
