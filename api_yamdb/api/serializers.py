from django.conf import settings
from rest_framework import serializers
from rest_framework.generics import get_oject_or_404
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User
from users.utils import username_validate


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
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
        fields = '__all__'
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_oject_or_404(Title, pk=title_id)
        # проверяем, хочет ли юзер отправить запрос на создание Отзыва
        if self.context['request'].user.method == 'POST':
            # проверяем есть ли отзыв у этого произведения
            # и принадлежит ли он автору запроса
            if Review.object.filter(title=title, pk=title_id):
                raise serializers.ValidationError(
                    'Нельзя добавить больше одного отзыва'
                )
        return data

    class Meta:
        fields = '__all__'
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(
        read_only=True, slug_field='username'
    )
    reviews = SlugRelatedField(
        slug_field='text', read_only=True
    )

    class Meta:
        fields = '__all__'
        model = Comment


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для обычных пользователей - не админов"""

    # username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Имя должно быть уникальным'),
            # username_validator
        ]
    )

    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='email должен быть уникальным'),
        ]
    )

    role = serializers.CharField(max_length=15, read_only=True)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]

    def validate(self, data):
        if not username_validate(data.get('username')):
            raise serializers.ValidationError(
                'Не допустимые символы в имени',
                'Имя может содержать только буквы, цифры и',
                'символы @/./+/-/_ '
            )
        return data


class AdminOrSuperAdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для пользователей админ и суперадмин.
    Этим пользователям доступно редактирование роли"""
    # username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Имя должно быть уникальным'),
            # username_validator
        ]
    )

    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='email должен быть уникальным')
        ]
    )

    role = serializers.CharField(max_length=15)

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role',
        ]

    def validate(self, data):
        if not username_validate(data.get('username')):
            raise serializers.ValidationError(
                'Не допустимые символы в имени',
                'Имя может содержать только буквы, цифры и',
                'символы @/./+/-/_ '
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор запроса авторизации"""

    # username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Имя должно быть уникальным'),
            # username_validator
        ]
    )

    email = serializers.EmailField(
        max_length=254,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='email должен быть уникальным'),
        ]
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email',
        ]


class TokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения токена по коду подтверждения"""
    username = serializers.CharField(
        max_length=150)

    confirmation_code = serializers.CharField(
        max_length=settings.MAX_CODE_LENGTH)

    class Meta:
        model = User
        fields = [
            'username',
            'confirmation_code',
        ]
