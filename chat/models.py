from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    subscribed_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='subscribers', blank=True)


class Chat(models.Model):
    chat_name = models.CharField(max_length=255)
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_user2')


class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)






