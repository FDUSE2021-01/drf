from users.serializers import UserSerializer
from users.serializers import MyTokenObtainPairSerializer
from users.permissions import IsMyself

from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator

from rest_framework import generics

from rest_framework_simplejwt.views import TokenObtainPairView


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    # Save hashed password instead of plain text
    def perform_create(self, serializer):
        password = make_password(password=serializer.validated_data['password'])
        send_mail('test_subject', '1234567', 'noreply@wanju.monster',[serializer.validated_data['email']])
        serializer.save(password=password, is_active= False)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMyself]

    # Save hashed password instead of plain text
    def perform_update(self, serializer):
        password = make_password(password=self.request.data['password'])
        serializer.save(password=password)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer



