from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель с дополнительным полем для подписок"""
    is_subscribed = models.BooleanField(default=False)


class Subscribe(models.Model):
    """Модель для подписок"""
    follow = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='follow'
    )
    follower = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower'
    )

    def __str__(self):
        return f"{self.follower} подписан на {self.follow}"
