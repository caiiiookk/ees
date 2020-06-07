# Generated by Django 2.2.10 on 2020-05-18 01:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat_app', '0006_auto_20200517_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='chat2user',
            name='activated',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chat2user',
            name='created',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='chatmodel',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 5, 18, 4, 26, 30, 969276)),
            preserve_default=False,
        ),
    ]
