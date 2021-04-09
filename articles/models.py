from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content_html = models.TextField()
    content_md = models.TextField()

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='articles'
    )

    class Meta:
        ordering = ['created']


class FileModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=256)
    file = models.FileField(upload_to='upload')

    author = models.ForeignKey(
        User,
        null=True,
        on_delete=models.CASCADE,
        related_name='files'
    )

    class Meta:
        ordering = ['created']


class ArticlesGame(models.Model):
    index = models.IntegerField(blank=True, null=True)
    href = models.TextField(blank=True, null=True)
    data_ds_appid = models.TextField(db_column='data-ds-appid', blank=True, null=True)
    data_ds_itemkey = models.TextField(db_column='data-ds-itemkey', blank=True, null=True)
    data_ds_tagids = models.TextField(db_column='data-ds-tagids', blank=True, null=True)
    data_ds_crtrids = models.TextField(db_column='data-ds-crtrids', blank=True, null=True)
    onmouseover = models.TextField(blank=True, null=True)
    onmouseout = models.TextField(blank=True, null=True)
    class_field = models.TextField(db_column='class', blank=True,
                                   null=True)  # Field renamed because it was a Python reserved word.
    data_search_page = models.IntegerField(db_column='data-search-page', blank=True, null=True)
    data_gpnav = models.TextField(db_column='data-gpnav', blank=True, null=True)
    item_name = models.TextField(blank=True, null=True)
    platform = models.TextField(blank=True, null=True)
    release_date = models.TextField(blank=True, null=True)
    rating_positive_ratio = models.TextField(blank=True, null=True)
    rating_count = models.TextField(blank=True, null=True)
    original_pricing = models.TextField(blank=True, null=True)
    pricing = models.TextField(blank=True, null=True)
    data_ds_bundleid = models.FloatField(db_column='data-ds-bundleid', blank=True, null=True)
    data_ds_bundle_data = models.TextField(db_column='data-ds-bundle-data', blank=True, null=True)
    data_ds_descids = models.TextField(db_column='data-ds-descids', blank=True, null=True)
    data_ds_packageid = models.FloatField(db_column='data-ds-packageid', blank=True, null=True)

    class Meta:
        db_table = 'articles_game'
