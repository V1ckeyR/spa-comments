import requests

import bleach
from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import Comment, Attachment, Reaction, User
from backend.config.settings import SECRET_GOOGLE_KEY


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9]+$',
            message='Username can only contain alphanumeric characters.')
        ])

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at']


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    captcha_token = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user_data = validated_data.get('user')
        user, _ = User.objects.get_or_create(**user_data)
        validated_data['user'] = user
        return super().create(validated_data)

    def validate_content(self, value):
        allowed_tags = ['a', 'code', 'i', 'strong']
        return bleach.clean(value, tags=allowed_tags)

    def validate_captcha_token(self, value):
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': SECRET_GOOGLE_KEY, 'response': value})
        results = response.json()
        if response.ok and results.get('success'):  # TODO: check the results.get('hostname') once actual hostname set up
            return value
        raise serializers.ValidationError('Invalid captcha token.')

    class Meta:
        model = Comment
        exclude = ['created_at', 'updated_at']


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        exclude = ['created_at', 'updated_at']


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
        read_only_fields = ['user']

