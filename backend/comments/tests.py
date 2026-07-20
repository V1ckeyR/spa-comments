from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch
from .models import Comment, User

class CommentCreateTests(APITestCase):
    def setUp(self):
        self.url = reverse('comment-list')