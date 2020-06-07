# Generated by Django 3.0.5 on 2020-05-15 23:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0005_auto_20200516_0254'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eesuser',
            name='date_joined',
        ),
        migrations.RemoveField(
            model_name='eesuser',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='eesuser',
            name='last_login',
        ),
        migrations.RemoveField(
            model_name='eesuser',
            name='last_name',
        ),
        migrations.AddField(
            model_name='eesuser',
            name='is_student',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='eesuser',
            name='is_teacher',
            field=models.BooleanField(default=False),
        ),
    ]
