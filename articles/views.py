from articles.models import Article, FileModel
from articles.serializers import ArticleSerializer, FileSerializer
from articles.permissions import IsAuthorOrReadOnly

from rest_framework import generics
from rest_framework import permissions
from rest_framework import response


class ArticleList(generics.ListCreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    # Filter configs
    filterset_fields = '__all__'
    search_fields = ['title', 'content_brief', 'content_md']
    ordering_fields = '__all__'

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class ArticleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]

    # Overrides retrieve() in rest_framework.mixins.RetrieveModelMixin
    # https://stackoverflow.com/a/56229309
    # https://stackoverflow.com/a/51737367
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.view_count = instance.view_count + 1
        instance.save(update_fields=("view_count",))
        serializer = self.get_serializer(instance)
        return response.Response(serializer.data)


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
