# Generated by Django 3.1.7 on 2021-04-29 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_myuser_icon'),
    ]

    operations = [
        migrations.AddField(
            model_name='myuser',
            name='verifycode',
            field=models.CharField(default='', max_length=254),
        ),
    ]