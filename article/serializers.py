from re import A
from rest_framework import serializers, status
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.utils.translation import gettext_lazy as _

from .models import Article


class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = '__all__'

    def validate(self, attrs):

        return super().validate(attrs)

    def create(self, validated_data):
        return super().create(validated_data)
