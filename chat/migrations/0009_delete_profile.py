# Generated by Django 4.2.3 on 2023-08-03 11:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_chat_permission_user1_chat_permission_user2'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]