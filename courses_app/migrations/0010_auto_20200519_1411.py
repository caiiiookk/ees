# Generated by Django 2.2.10 on 2020-05-19 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0009_auto_20200518_1850'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question2Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group', models.TextField()),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses_app.QuestionModel')),
            ],
        ),
        migrations.CreateModel(
            name='Test2Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses_app.QuestionModel')),
            ],
        ),
        migrations.AlterField(
            model_name='testsmodel',
            name='name',
            field=models.CharField(max_length=60),
        ),
        migrations.DeleteModel(
            name='Question2Number',
        ),
        migrations.AddField(
            model_name='test2questions',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='courses_app.TestsModel'),
        ),
    ]
