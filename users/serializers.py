from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.serializers import AuthTokenSerializer


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'login', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super().create(validated_data)


class CustomAuthTokenSerializer(AuthTokenSerializer):
    login = serializers.CharField(write_only=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        if login and password:
            user = authenticate(request=self.context.get('request'),
                                username=login,
                                password=password)
            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Must include "login" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
