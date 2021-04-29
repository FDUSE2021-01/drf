from rest_framework import serializers
from articles.models import Article, FileModel


class ArticleSerializer(serializers.ModelSerializer):

    # https://stackoverflow.com/a/37944195
    favorite = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author', 'view_count', 'favorite']

    def get_favorite(self, obj):
        user = self.context['request'].user
        if user.is_authenticated and obj in user.favorite_articles.all():
            return True
        else:
            return False


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileModel
        fields = '__all__'
        read_only_fields = ['author']
