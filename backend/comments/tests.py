from datetime import timedelta
from unittest.mock import patch

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Comment, User


class CommentAPITestCase(APITestCase):
    def setUp(self):
        self.list_url = reverse('comment-list')

    def valid_payload(self, **overrides):
        data = {
            'reply_to': None,
            'content': 'Hello, world',
            'user': {'username': 'John_Doe', 'email': 'john@comments.com'},
            'captcha_token': 'somerandomtoken',
        }
        data.update(overrides)
        return data

    def mock_captcha_success(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {'success': True}

    def mock_captcha_failure(self, mock_post):
        mock_post.return_value.ok = True
        mock_post.return_value.json.return_value = {'success': False}

    def create_comment_via_api(self, mock_post, **overrides):
        self.mock_captcha_success(mock_post)
        return self.client.post(
            self.list_url,
            data=self.valid_payload(**overrides),
            format='json',
        )


class CommentCreateTests(CommentAPITestCase):
    @patch('requests.post')
    def test_create_comment(self, mock_post):
        self.mock_captcha_success(mock_post)
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(User.objects.first().email, 'john@comments.com')
        self.assertNotIn('captcha_token', response.data)

    @patch('requests.post')
    def test_create_comment_bad_captcha(self, mock_post):
        self.mock_captcha_failure(mock_post)
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    @patch('requests.post')
    def test_create_comment_bad_content_only(self, mock_post):
        self.mock_captcha_success(mock_post)
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(content='<script></script><b></b>'),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    @patch('requests.post')
    def test_create_comment_bad_content_partial(self, mock_post):
        self.mock_captcha_success(mock_post)
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(
                content='<script>alert("xss")</script><b>text</b><i>Cursive text</i>',
            ),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(
            Comment.objects.first().content,
            'alert("xss")text<i>Cursive text</i>',
        )

    @patch('requests.post')
    def test_create_comment_whitespace_only_content(self, mock_post):
        self.mock_captcha_success(mock_post)
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(content='   \t  '),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    @patch('requests.post')
    def test_create_comment_allowed_html_tags(self, mock_post):
        self.mock_captcha_success(mock_post)
        content = (
            '<a href="https://example.com">link</a>'
            '<code>code</code>'
            '<strong>bold</strong>'
            '<i>italic</i>'
        )
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(content=content),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.first().content, content)

    @patch('requests.post')
    def test_create_comment_invalid_username(self, mock_post):
        self.mock_captcha_success(mock_post)
        response = self.client.post(
            self.list_url,
            data=self.valid_payload(user={'username': 'bad user!', 'email': 'john@comments.com'}),
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Comment.objects.count(), 0)

    @patch('requests.post')
    def test_create_comment_reuses_existing_user(self, mock_post):
        user = User.objects.create(username='John_Doe', email='john@comments.com')
        response = self.create_comment_via_api(mock_post)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Comment.objects.first().user_id, user.id)

    @patch('requests.post')
    def test_create_comment_reply(self, mock_post):
        parent_response = self.create_comment_via_api(
            mock_post,
            content='Parent comment',
        )
        parent_id = parent_response.data['id']

        response = self.create_comment_via_api(
            mock_post,
            content='Reply comment',
            reply_to=parent_id,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        reply = Comment.objects.get(content='Reply comment')
        self.assertEqual(reply.reply_to_id, parent_id)


class CommentListTests(CommentAPITestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create(username='Jane_Doe', email='jane@comments.com')
        self.comment = Comment.objects.create(
            content='Existing comment',
            user=self.user,
        )

    def test_list_comments(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(len(response.data['results']), 1)
        self.assertEqual(response.data['results'][0]['content'], 'Existing comment')
        self.assertEqual(response.data['results'][0]['user']['email'], 'jane@comments.com')

    def test_retrieve_comment(self):
        detail_url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.get(detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.comment.id)
        self.assertEqual(response.data['content'], 'Existing comment')

    def test_list_comments_ordered_by_newest_first(self):
        now = timezone.now()
        Comment.objects.create(content='Older comment', user=self.user)
        Comment.objects.create(content='Newer comment', user=self.user)
        Comment.objects.filter(content='Older comment').update(created_at=now - timedelta(hours=1))
        Comment.objects.filter(content='Newer comment').update(created_at=now + timedelta(hours=1))

        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        contents = [item['content'] for item in response.data['results']]
        self.assertEqual(contents[0], 'Newer comment')
