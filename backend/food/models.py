from django.db import models
from ..users.models import User


class recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    name = models.CharField()
    image = models.ImageField(
        upload_to='food/',
        blank=True,
        null=True
    )
    description = models.TextField()
    cooking_time = models.PositiveIntegerField()


class Tag(models.Model):
    name = models.CharField(
        unique=True
    )
    color = models.CharField(
        unique=True,
        max_length=7
    )
    slug = models.SlugField(unique=True)


class Ingredient(models.Model):
    name = models.CharField()
    count = models.PositiveIntegerField()
    unit = models.CharField()
