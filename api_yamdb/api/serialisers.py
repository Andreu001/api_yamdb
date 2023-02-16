from rest_framework import serializers
# from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator
from users.models import User
from users.validators import UnicodeUsernameValidator
from django.conf import settings
from django.core.validators import validate_email
from users.utils import username_validate

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для обычных пользователей - не админов"""

    #username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Имя должно быть уникальным'),
            #username_validator
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
                f'Не допустимые символы в имени',
                f'Имя может содержать только буквы, цифры и',
                f'символы @/./+/-/_ '
            )
        return data


class AdminOrSuperAdminUserSerializer(serializers.ModelSerializer):
    """Сериализатор модели User для пользователей админ и суперадмин.
    Этим пользователям доступно редактирование роли"""
    #username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Имя должно быть уникальным'),
            #username_validator
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
                f'Не допустимые символы в имени',
                f'Имя может содержать только буквы, цифры и',
                f'символы @/./+/-/_ '
            )
        return data


class SignUpSerializer(serializers.ModelSerializer):
    """Сериализатор запроса авторизации"""

    #username_validator = UnicodeUsernameValidator()

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message='Имя должно быть уникальным'),
            #username_validator
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

