# Generated by Django 3.0.6 on 2020-05-26 23:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0025_delete_test2user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursemodel',
            name='name',
            field=models.CharField(max_length=250),
        ),
    ]