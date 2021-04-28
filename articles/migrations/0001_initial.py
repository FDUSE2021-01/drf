# Generated by Django 3.1.7 on 2021-04-28 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(blank=True, default='', max_length=100)),
                ('content_html', models.TextField()),
                ('content_md', models.TextField()),
                ('content_brief', models.TextField(blank=True, default='')),
                ('img_src', models.CharField(max_length=1000)),
                ('view_count', models.PositiveIntegerField(default=0)),
            ],
            options={
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='ArticlesGame',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.IntegerField(blank=True, null=True)),
                ('href', models.TextField(blank=True, null=True)),
                ('data_ds_appid', models.TextField(blank=True, db_column='data-ds-appid', null=True)),
                ('data_ds_itemkey', models.TextField(blank=True, db_column='data-ds-itemkey', null=True)),
                ('data_ds_tagids', models.TextField(blank=True, db_column='data-ds-tagids', null=True)),
                ('data_ds_crtrids', models.TextField(blank=True, db_column='data-ds-crtrids', null=True)),
                ('onmouseover', models.TextField(blank=True, null=True)),
                ('onmouseout', models.TextField(blank=True, null=True)),
                ('class_field', models.TextField(blank=True, db_column='class', null=True)),
                ('data_search_page', models.IntegerField(blank=True, db_column='data-search-page', null=True)),
                ('data_gpnav', models.TextField(blank=True, db_column='data-gpnav', null=True)),
                ('item_name', models.TextField(blank=True, null=True)),
                ('platform', models.TextField(blank=True, null=True)),
                ('release_date', models.TextField(blank=True, null=True)),
                ('rating_positive_ratio', models.TextField(blank=True, null=True)),
                ('rating_count', models.TextField(blank=True, null=True)),
                ('original_pricing', models.TextField(blank=True, null=True)),
                ('pricing', models.TextField(blank=True, null=True)),
                ('data_ds_bundleid', models.FloatField(blank=True, db_column='data-ds-bundleid', null=True)),
                ('data_ds_bundle_data', models.TextField(blank=True, db_column='data-ds-bundle-data', null=True)),
                ('data_ds_descids', models.TextField(blank=True, db_column='data-ds-descids', null=True)),
                ('data_ds_packageid', models.FloatField(blank=True, db_column='data-ds-packageid', null=True)),
            ],
            options={
                'db_table': 'articles_game',
            },
        ),
        migrations.CreateModel(
            name='FileModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=256)),
                ('file', models.FileField(upload_to='upload')),
            ],
            options={
                'ordering': ['created'],
            },
        ),
    ]
