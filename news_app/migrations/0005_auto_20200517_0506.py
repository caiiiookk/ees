# Generated by Django 3.0.6 on 2020-05-17 02:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news_app', '0004_auto_20200516_0437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsmodel',
            name='name',
            field=models.CharField(blank=True, max_length=2500),
        ),
    ]
