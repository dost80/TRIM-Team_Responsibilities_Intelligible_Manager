# Generated by Django 2.0.2 on 2018-03-20 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trim_app', '0002_auto_20180320_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(blank=True, default=None),
        ),
        migrations.AlterField(
            model_name='task',
            name='end_date',
            field=models.DateTimeField(blank=True, default=None),
        ),
    ]