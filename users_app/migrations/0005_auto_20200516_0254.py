# Generated by Django 3.0.5 on 2020-05-15 23:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users_app', '0004_auto_20200516_0252'),
    ]

    operations = [
        migrations.RenameField(
            model_name='eesuser',
            old_name='is_staff',
            new_name='is_employee',
        ),
        migrations.RemoveField(
            model_name='eesuser',
            name='is_active',
        ),
    ]
