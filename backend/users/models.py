from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Моедль с дополнительным полем для подписок"""
    is_subscribed = models.BooleanField(default=False)
