from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)

    # Дополнительные методы, если необходимо

    def __str__(self):
        return self.username