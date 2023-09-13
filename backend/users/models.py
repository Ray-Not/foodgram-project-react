from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_subscribed = models.BooleanField(editable=False, default=False)
