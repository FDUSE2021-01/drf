# Generated by Django 3.1.7 on 2021-04-10 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0007_auto_20210410_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='content_brief',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='article',
            name='img_src',
            field=models.CharField(max_length=100),
        ),
    ]