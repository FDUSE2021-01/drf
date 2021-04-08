from articles.models import Article, FileModel
from articles.serializers import ArticleSerializer, FileSerializer
from articles.permissions import IsAuthorOrReadOnly

from rest_framework import generics
from rest_framework import permissions
from rest_framework import viewsets

class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]



# class FileViewSet(viewsets.ModelViewSet):
#     queryset = FileModel.objects.all()
#     serializer_class = FileSerializer
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly,
#                           IsAuthorOrReadOnly]

class FileModelList(generics.ListCreateAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class FileModelDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FileModel.objects.all()
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]