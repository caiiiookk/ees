# Generated by Django 3.0.6 on 2020-05-17 02:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat_app', '0003_chat_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Chat',
            new_name='ChatModel',
        ),
        migrations.RenameModel(
            old_name='Message',
            new_name='MessageModel',
        ),
        migrations.RenameField(
            model_name='chatmodel',
            old_name='admin_id',
            new_name='admin',
        ),
    ]
