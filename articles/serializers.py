from rest_framework import serializers
from articles.models import Article, FileModel


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author', 'view_count']

class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'
        read_only_fields = ['author']