from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    content = models.TextField()

    class Meta:
        ordering = ['created']
