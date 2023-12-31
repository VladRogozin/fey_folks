from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null=True, blank=True)
    city = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=300, blank=True)
    avatar = models.ImageField(upload_to='avatars/')  # New field for avatar photo
    is_online = models.BooleanField(default=False)

    # Дополнительные методы, если необходимо


    def __str__(self):
        return self.username
