# Generated by Django 3.1.7 on 2021-04-29 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_myuser_favorite_articles'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='icon',
            field=models.ImageField(default='pictures/a.png', upload_to='pictures/'),
        ),
    ]
