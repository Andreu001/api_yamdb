from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import AccessToken
from users.permissions import IsOwner, IsAdminOrSuperAdmin
from django.shortcuts import get_object_or_404
from users.models import User
from django.conf import settings
from rest_framework.exceptions import ValidationError

from users.utils import (
    get_unique_confirmation_code,
    sent_email_with_confirmation_code,
)

from api.serialisers import (
    UserSerializer,
    AdminOrSuperAdminUserSerializer,
    SignUpSerializer,
    TokenSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Класс для работы с пользователем(ми)"""

    http_method_names = ['get', 'post', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated, IsAdminOrSuperAdmin]
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
            permission_classes=[IsAuthenticated,],
    )
    def me(self, request):
        """Добавление users/me для получения и изменении информации в
        своем профиле"""
    
        user = get_object_or_404(User, id=request.user.id)

        if request.method == 'GET':
            serializer = self.get_serializer(user, many=False)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response("Не допустимы тип запроса", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def SignUpView(request):
    """Авторизация"""

    if request.method == 'POST':
        # Создаём объект сериализатора
        # и передаём в него данные из POST-запроса
        serializer = SignUpSerializer(data=request.data, many=False)
        #serializer.is_valid(raise_exception=True)
        # Если полученные данные валидны —
        #user_email = serializer.validated_data['email']
        #username = serializer.validated_data['username']

        #serializer.save()
        is_user = User.objects.filter(
            username=request.data.get('username'),
            email=request.data.get('email'))
        if is_user.exists():
            return Response('У вас уже есть регистрация', status=status.HTTP_200_OK)
        # Формируем код подтверждения
        serializer.is_valid(raise_exception=True)
        # Если полученные данные валидны —
        user_email = serializer.validated_data['email']
        username = serializer.validated_data['username']
        serializer.is_valid(raise_exception=True)
        if username == 'me':
            return Response('Задайте другое имя', status=status.HTTP_400_BAD_REQUEST)
        confirm_code = get_unique_confirmation_code()
        # После успешного сохранения
        user, _created = User.objects.get_or_create(
            username=username,
            email=user_email
        )
        user.confirmation_code = confirm_code
        user.save()
        # отправляем письмо с кодом подтверждения
        sent_email_with_confirmation_code(user_email, confirm_code)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def TokenView(request):
    """Отправка токена"""

    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )

    if user.confirmation_code == serializer.validated_data['confirmation_code']:
        return Response(
            {'token': str(AccessToken.for_user(user))},
            status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
