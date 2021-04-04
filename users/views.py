from users.serializers import UserSerializer
from users.permissions import IsMyself

from django.contrib.auth.models import User

from rest_framework import generics


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsMyself]
