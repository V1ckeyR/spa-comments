from django.db import models
from django.db.models import F


class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(TimeModel):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    home_page = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=['username']),  # to filter by username quickly
        ]


class Attachment(TimeModel):
    url = models.URLField()
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)

    class Meta:
        indexes = [
            models.Index(fields=['comment', 'created_at']),  # optimize query to get attachments for a comment
        ]


class Reaction(models.Model):
    class ReactionType(models.IntegerChoices):
        LIKE = 1, 'Like'
        DISLIKE = -1, 'Dislike'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE)
    reaction = models.IntegerField(choices=ReactionType.choices)

    class Meta:
        unique_together = ('user', 'comment')
        indexes = [
            models.Index(fields=['comment', 'reaction']),  # optimize query to get reactions for a comment
        ]

    def __str__(self):
        return f'{self.user.username} {self.reaction} {self.comment.id}'


class Comment(TimeModel):
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    reply_to = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)


    class Meta:
        indexes = [
            models.Index(F('created_at').desc(), name='cmt_created_desc_idx'),  # optimize query to get latest comments
            models.Index(F('reply_to'), F('created_at').desc(), name='cmt_reply_created_idx'),  # optimize query to get latest replies for a comment
        ]


    def __str__(self):
        return f'Comment {self.id} by {self.user.username}'

    @property
    def get_reactions(self):
        return self.reaction_set.aggregate(models.Sum('reaction'))['reaction__sum'] or 0
