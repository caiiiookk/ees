# Generated by Django 2.2.10 on 2020-05-21 01:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0022_auto_20200520_1803'),
    ]

    operations = [
        migrations.RenameField(
            model_name='triesmodel',
            old_name='date_submited',
            new_name='date_submitted',
        ),
    ]
