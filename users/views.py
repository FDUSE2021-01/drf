from .serializers import UserSerializer, MyTokenObtainPairSerializer, UserChangePasswordSerializer
from .permissions import IsMyself
from .models import MyUser

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics, status, response, permissions
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView

from . import models

from articles.models import Article
from articles.serializers import ArticleSerializer
from random import Random


def random_str(randomlength=6):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


class UserActivation(APIView):
    # serializer_class = UserSerializer
    def get(self, request, format=None):
        """\
        activate user with token
        """
        if not request.GET.get('token'):
            return response.Response('token required', status=status.HTTP_400_BAD_REQUEST)
        try:
            target = MyUser.objects.get(activationtoken__activationToken=request.GET['token'])
        except MyUser.DoesNotExist:
            target = None
        if target:
            target.is_active = True
            target.save()
        return response.Response('successful')


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    # Save hashed password instead of plain text
    # https://stackoverflow.com/a/27471503
    def perform_create(self, serializer):
        password = make_password(password=serializer.validated_data['password'])
        instance = serializer.save(password=password, is_active=False)
        token = default_token_generator.make_token(instance)
        models.ActivationToken.objects.create(user=instance, activationToken=token)
        send_mail('test_subject', f'http://wanju.monster/activation.html?token={token}', 'noreply@wanju.monster',
                  [serializer.validated_data['email']])


class UserPostVerifycode(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMyself]

    def perform_update(self, serializer):
        '''
            Sent verification code and save it.
        '''
        code = random_str(6)
        send_mail('test_code', code, 'noreply@wanju.monster',
                  [serializer.validated_data['email']])
        serializer.save(verifycode=code)


class UserDealVerifycode(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        code = request.data.get('verifycode')
        if request.user.verifycode == code:
            return Response(data={}, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': 'Verified error'}, status=status.HTTP_404_NOT_FOUND)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMyself]

    # Save hashed password instead of plain text
    # https://stackoverflow.com/a/34191977
    def perform_update(self, serializer):
        if 'password' in self.request.data:
            password = make_password(password=self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()


# change password when logged in
class UserChangePassword(generics.GenericAPIView):
    queryset = MyUser.objects.all()
    serializer_class = UserChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated, IsMyself]

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # Check old password
        if not self.object.check_password(serializer.data.get("old_password")):
            return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
        self.object.set_password(serializer.data.get("new_password"))
        self.object.save()
        return response.Response('Password updated successfully')


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Using many-to-many field in User model to manage favorites
# https://stackoverflow.com/questions/63361830/is-this-the-correct-way-to-add-post-to-favourites-using-django-rest-framework
# https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/
class UserFavoriteArticlesListCreate(generics.ListCreateAPIView):
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return user.favorite_articles.all()

    def post(self, request, format=None):
        article = get_object_or_404(Article, id=request.data.get('article_id'))
        if article not in request.user.favorite_articles.all():
            article.fav_count = article.fav_count + 1
            article.save(update_fields=("fav_count",))
            request.user.favorite_articles.add(article)
        return Response(data={'user_id': request.user.id, 'article_id': article.id}, status=status.HTTP_200_OK)


class UserFavoriteArticlesRetrieveDestroy(APIView):
    permission_classes = [permissions.IsAuthenticated, IsMyself]

    def get(self, request, pk, format=None):
        article = get_object_or_404(Article, id=pk)
        if article in request.user.favorite_articles.all():
            return Response(data={'user_id': request.user.id, 'article_id': article.id}, status=status.HTTP_200_OK)
        else:
            return Response(data={'detail': '未收藏该文章'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        article = get_object_or_404(Article, id=pk)
        if article in request.user.favorite_articles.all():
            article.fav_count = article.fav_count - 1
            article.save(update_fields=("fav_count",))
            request.user.favorite_articles.remove(article)
            return Response(data=None, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(data={'detail': '未收藏该文章'}, status=status.HTTP_404_NOT_FOUND)
