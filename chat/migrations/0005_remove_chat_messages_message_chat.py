# Generated by Django 4.2.3 on 2023-07-30 19:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0004_message_alter_chat_chat_name_alter_chat_user1_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='messages',
        ),
        migrations.AddField(
            model_name='message',
            name='chat',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='chat.chat'),
            preserve_default=False,
        ),
    ]