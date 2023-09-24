from django.db import models
from users.models import User


class Recipe(models.Model):
    """Модель рецептов"""
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор',
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название рецепта'
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
        verbose_name='Время готовки (мин.)',
    )

    def __str__(self):
        return self.name


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
    CHOICES = (
        ('kilogramm', 'кг.'),
        ('gramm', 'гр.'),
        ('mililitre', 'мл.'),
        ('litre', 'л.'),
        ('tablespoon', 'стл. л.'),
        ('piece', 'шт.'),
    )
    name = models.CharField(
        max_length=128,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=128,
        choices=CHOICES,
        verbose_name='Единица измерения',
    )

    def __str__(self):
        return self.name


class RecipesIngredient(models.Model):
    """Связываящая модель Рецепт->Ингредиент"""
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
    )
    count = models.PositiveIntegerField(
        verbose_name='Количество ингредиента',
    )

    def __str__(self):
        return f'{self.recipe} с использованием {self.ingredient}'
