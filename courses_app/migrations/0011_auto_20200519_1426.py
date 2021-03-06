# Generated by Django 2.2.10 on 2020-05-19 11:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0010_auto_20200519_1411'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='test2questions',
            name='question',
        ),
        migrations.RemoveField(
            model_name='test2questions',
            name='test',
        ),
        migrations.AddField(
            model_name='checkorradioanswermodel',
            name='question',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses_app.QuestionModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='questionmodel',
            name='test',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='courses_app.TestsModel'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Question2Answer',
        ),
        migrations.DeleteModel(
            name='Test2Questions',
        ),
    ]
