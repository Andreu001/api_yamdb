from api.filters import TitleFilter
# from django.conf import settings
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.filters import SearchFilter
# from rest_framework.exceptions import ValidationError
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title
from users.models import User
from users.permissions import IsAdminOrSuperAdmin
from users.utils import (get_unique_confirmation_code,
                         sent_email_with_confirmation_code)

from .mixins import ModelMixinSet
from api.permissions import (IsAdminUserOrReadOnly,
                             AdminModeratorAuthorPermission)
from api.serializers import (AdminOrSuperAdminUserSerializer,
                             CategorySerializer,
                             CommentSerializer, GenreSerializer,
                             ReviewSerializer,
                             SignUpSerializer, TitleReadSerializer,
                             TitleWriteSerializer, TokenSerializer,
                             UserSerializer)


class CategoryViewSet(ModelMixinSet):
    """
    Получить список всех категорий. Права доступа: Доступно без токена
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(ModelMixinSet):
    """
    Получить список всех жанров. Права доступа: Доступно без токена
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    """
    Получить список всех объектов. Права доступа: Доступно без токена
    """
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')
    ).all()
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователем(ми)"""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminOrSuperAdmin]
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    def get_serializer_class(self):
        """выбор сериализатора в зависимости от типа пользователя"""

        if (
            self.request.user.role != 'admin'
            or self.request.user.is_superuser
        ):
            return UserSerializer
        return AdminOrSuperAdminUserSerializer

    @action(methods=['get', 'patch'],
            detail=False,
            permission_classes=[IsAuthenticated],
            )
    def me(self, request):
        """Добавление users/me для получения и изменении информации в
        своем профиле"""

        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Не допустимы тип запроса",
                        status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def signupview(request):
    """Авторизация"""

    if request.method == 'POST':
        user_request = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'))
        if user_request.exists():
            return Response(
                'У вас уже есть регистрация',
                status=status.HTTP_200_OK
            )
        if User.objects.filter(email=request.data.get('email')):
            return Response(
                'Такая почта уже зарегистриована',
                status=status.HTTP_400_BAD_REQUEST
            )
        if User.objects.filter(username=request.data.get('username')):
            return Response(
                'Такое имя уже занято уже зарегистриовано',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        serializer.is_valid(raise_exception=True)
        if username == 'me':
            return Response(
                'Задайте другое имя', status=status.HTTP_400_BAD_REQUEST
            )
        # Формируем код подтверждения
        confirm_code = get_unique_confirmation_code()
        user, _created = User.objects.get_or_create(
            username=username,
            email=user_email)
        user.confirmation_code = confirm_code
        user.save()
        # отправляем письмо с кодом подтверждения
        sent_email_with_confirmation_code(user_email, confirm_code)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def tokenview(request):
    """Отправка токена"""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if user.confirmation_code == (
        serializer.validated_data['confirmation_code']
    ):
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [AdminModeratorAuthorPermission]  # добавить ограничения

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [AdminModeratorAuthorPermission]  # добавить ограничения


    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(
            Review,
            id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
