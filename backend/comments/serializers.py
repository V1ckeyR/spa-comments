import requests

import bleach
from django.conf import settings
from rest_framework import serializers
from django.core.validators import RegexValidator

from .models import Comment, Attachment, Reaction, User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[RegexValidator(
            regex=r'^[a-zA-Z0-9_]+$',
            message='Username can only contain alphanumeric characters.')
        ])

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at']
        extra_kwargs = {
            'email': {'validators': []},
        }


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    captcha_token = serializers.CharField(write_only=True)

    def create(self, validated_data):
        validated_data.pop('captcha_token', None)
        user_data = validated_data.pop('user')
        user, _ = User.objects.get_or_create(**user_data)
        validated_data['user'] = user
        return super().create(validated_data)

    def validate_content(self, value):
        allowed_tags = ['a', 'code', 'i', 'strong']
        cleaned_value = bleach.clean(value, tags=allowed_tags, strip=True).strip()
        if not cleaned_value:
            raise serializers.ValidationError('Comment content cannot be empty')

        return  cleaned_value

    def validate_captcha_token(self, value):
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data={'secret': settings.SECRET_GOOGLE_KEY, 'response': value})
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

