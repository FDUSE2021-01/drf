from users.serializers import UserSerializer
from users.serializers import MyTokenObtainPairSerializer
from users.permissions import IsMyself

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(password=self.request.data['password'])
        serializer.save(password=password)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMyself]

    def perform_update(self, serializer):
        password = make_password(password=self.request.data['password'])
        serializer.save(password=password)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



