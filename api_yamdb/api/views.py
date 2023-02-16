from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
# from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from reviews.models import Review, Title

from .serializers import CommentSerializer, ReviewSerializer

User = get_user_model()


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # filter_backends = [DjangoFilterBackend]

    permission_classes = []  # добавить ограничения

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.rewiews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    permission_classes = []  # добавить ограничения
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review.comments.all()
        return new_queryset

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        title_id = self.kwargs.get('title_id')
        review = get_object_or_404(Review, id=review_id, title=title_id)
        serializer.save(author=self.request.user, review=review)
