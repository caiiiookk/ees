# Generated by Django 2.2.10 on 2020-05-18 01:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses_app', '0004_pagesmodel_section2documents_section2pages_section2sections_section2tests_sectionmodel_test2user_tes'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('document', models.FileField(upload_to='documents/')),
            ],
        ),
        migrations.AlterField(
            model_name='section2documents',
            name='documents',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='courses_app.DocumentsModel'),
        ),
    ]
