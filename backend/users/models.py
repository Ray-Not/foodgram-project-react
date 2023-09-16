from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Дополнительное поле для подписок"""
    is_subscribed = models.BooleanField(default=False)
