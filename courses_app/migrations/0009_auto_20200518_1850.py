# Generated by Django 2.2.10 on 2020-05-18 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0008_auto_20200518_1640'),
    ]

    operations = [
        migrations.RenameField(
            model_name='checkorradioanswermodel',
            old_name='content',
            new_name='answer',
        ),
        migrations.RemoveField(
            model_name='coursemodel',
            name='is_orientationable',
        ),
    ]
