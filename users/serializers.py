from users.models import MyUser
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    # Change email field to "required"
    email = serializers.EmailField(allow_blank=False, label='电子邮箱地址', max_length=254, required=True)

    class Meta:
        model = MyUser
        fields = '__all__'
        read_only_fields = ['id',
                            'groups',
                            'user_permissions',
                            'is_staff',
                            'is_active',
                            'is_superuser',
                            'last_login',
                            'date_joined',
                            'favorite_articles']
        extra_kwargs = {
            # Do not show passwords to the client
            'password': {
                'write_only': True,
            },
        }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['id'] = self.user.id
        data['username'] = self.user.username
        return data

