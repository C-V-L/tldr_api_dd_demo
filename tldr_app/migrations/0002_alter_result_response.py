# Generated by Django 4.2.1 on 2023-05-17 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tldr_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='result',
            name='response',
            field=models.JSONField(default=dict),
        ),
    ]
