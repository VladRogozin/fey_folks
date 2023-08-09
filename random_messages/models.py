from django.conf import settings

from django.db import models


class RandomMessage(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Message #{self.id} from {self.sender} to {self.recipient}"


class RandomTips(models.Model):
    chat_name = models.CharField(max_length=32)
    text = models.CharField(max_length=255)


class RandomPost(models.Model):
    author_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='author_random_post')
    title = models.CharField(max_length=100)
    description = models.TextField()
    photo = models.ImageField(upload_to='post_photos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Добавленное поле для даты создания

    def __str__(self):
        return self.title

