from django.db import models
from django.contrib.auth.models import AbstractUser
from articles.models import Article


# Create your models here.

class MyUser(AbstractUser):
    # https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
    favorite_articles = models.ManyToManyField(Article, related_name='favorite_articles', blank=True)
    icon = models.ImageField(upload_to='pictures/', default='pictures/a.png')
    verifycode = models.CharField(max_length=254, default='')


class ActivationToken(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    activationToken = models.CharField(max_length=255)

    def __str__(self):
        return self.activationToken
