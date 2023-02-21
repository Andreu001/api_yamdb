from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator, UniqueValidator

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import CHOICE_ROLES, User
from users.utils import (email_validate, username_validate)


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        lookup_field = 'slug'
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        lookup_field = 'slug'
        fields = ('name', 'slug')


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'rating',
                  'description',
                  'genre',
                  'category')
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id',
                  'name',
                  'year',
                  'description',
                  'genre',
                  'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def validate(self, data):
        request = self.context['request']
        author = request.user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, pk=title_id)
        if request.method == 'POST':
            if Review.objects.filter(title=title, author=author).exists():
                raise serializers.ValidationError(
                    'Нельзя добавить больше одного отзыва'
                )
        return data

    class Meta:
        fields = (
            'id', 'text', 'author',
            'score', 'pub_date',
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = (
            'id', 'text', 'author',
            'pub_date',
        )
        read_only_fields = (
            'id', 'author', 'pub_date',
        )
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для обычных пользователей - не админов"""

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

    def validate_username(self, value):
        username_validate(value)
        return value

    def validate_email(self, value):
        email_validate(value)
        return value


class MeSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для редактирования профайла"""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)
    role = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role'
        )

        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        username_validate(value)
        return value

    def validate_email(self, value):
        email_validate(value)
        return value


class AdminOrSuperAdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для пользователей админ и суперадмин.
    Этим пользователям доступно редактирование роли"""

    email = serializers.EmailField(max_length=254)
    username = serializers.CharField(max_length=150)
    role = serializers.CharField(max_length=15, default='user')

    class Meta:
        model = User
        fields = (
            'email',
            'username',
            'first_name',
            'last_name',
            'bio',
            'role',
        )

        validators = (
            UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            ),
        )

    def validate_username(self, value):
        username_validate(value)
        return value

    def validate_email(self, value):
        email_validate(value)
        return value

    def validate(self, data):
        role = str(data.get('role'))
        if (any(role in i for i in CHOICE_ROLES)):
            raise serializers.ValidationError(
                'Задана не существующая роль'
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор запроса авторизации"""

    username = serializers.CharField(
        max_length=150,
        validators=[UniqueValidator(queryset=User.objects.all())]
    ),
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = (
            'username',
            'email',
        )

    def validate_username(self, value):
        username_validate(value)
        return value

    def validate_email(self, value):
        email_validate(value)
        return value


class TokenSerializer(serializers.Serializer):
    """Сериализатор получения токена по коду подтверждения"""
    username = serializers.CharField(
        max_length=150)

    confirmation_code = serializers.CharField(
        max_length=settings.MAX_CODE_LENGTH, write_only=True)

    class Meta:
        fields = [
            'username',
            'confirmation_code',
        ]

    def validate_username(self, value):
        username_validate(value)
        return value

    def validate_email(self, value):
        email_validate(value)
        return value
