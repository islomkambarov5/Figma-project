from django.contrib.auth.models import User
from rest_framework.fields import HiddenField, CurrentUserDefault
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from qurilish_app.models import Posts, Comments


class PostSerializer(ModelSerializer):
    author = HiddenField(default=CurrentUserDefault())

    class Meta:
        model = Posts
        fields = ["title", "context", 'author']


class CommentSerializer(ModelSerializer):
    user = HiddenField(default=CurrentUserDefault())
    post = HiddenField(default=None)

    class Meta:
        model = Comments
        fields = ["user", "text", "post", "created_at"]


class LogInSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password"]
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''))

        return user


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PasswordResetViaEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
