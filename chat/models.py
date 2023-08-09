from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models




class Chat(models.Model):
    chat_name = models.CharField(max_length=255)
    user1 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_user1')
    user2 = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='chat_user2')
    permission_user1 = models.BooleanField(default=False)
    permission_user2 = models.BooleanField(default=False)
    background_image_1 = models.ImageField(upload_to='chat_backgrounds/', blank=True, null=True)
    background_image_2 = models.ImageField(upload_to='chat_backgrounds/', blank=True, null=True)

    def has_both_permissions(self):
        return self.permission_user1 and self.permission_user2

    @property
    def last_message(self):
        return self.message_set.order_by('-timestamp').first()

    @property
    def last_message_timestamp(self):
        last_message = self.last_message
        return last_message.timestamp if last_message else None

class Message(models.Model):
    content = models.TextField()
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)






