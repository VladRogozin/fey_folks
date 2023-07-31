# Generated by Django 4.2.3 on 2023-07-30 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chat',
            old_name='chatName',
            new_name='chat_name',
        ),
        migrations.AlterField(
            model_name='chat',
            name='messages',
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]
