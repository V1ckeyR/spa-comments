from rest_framework.viewsets import ModelViewSet

from .models import Comment
from .serializers import CommentSerializer


class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return (
            Comment.objects
            .all()
            .order_by('-created_at')
            .prefetch_related('reaction_set', 'attachment_set')
        )
