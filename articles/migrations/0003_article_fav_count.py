# Generated by Django 3.1.7 on 2021-04-28 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20210428_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='fav_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]