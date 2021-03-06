# Generated by Django 3.0.6 on 2020-05-16 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0010_auto_20200516_0825'),
    ]

    operations = [
        migrations.AddField(
            model_name='eesuser',
            name='can_change_email',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='eesuser',
            name='can_change_first_name',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='eesuser',
            name='can_change_last_name',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='eesuser',
            name='can_change_username',
            field=models.BooleanField(default=False),
        ),
    ]
