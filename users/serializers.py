from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(allow_blank=False, label='电子邮件地址', max_length=254, required=True)

    def create(self, validated_data):
        user = User(username=validated_data['username'],
                    email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['id',
                            'groups',
                            'user_permissions',
                            'is_staff',
                            'is_active',
                            'is_superuser',
                            'last_login',
                            'date_joined']
