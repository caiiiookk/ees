# Generated by Django 2.2.10 on 2020-05-18 05:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0005_auto_20200518_0457'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursemodel',
            name='section',
            field=models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses_app.SectionModel'),
            preserve_default=False,
        ),
    ]
