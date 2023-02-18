from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомная модель пользователя унаследованная от AbstractUser
    для расширения атрибутов пользователя"""

    CHOICE_ROLES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin')
    )

    username = models.CharField(
        'Пользователь',
        max_length=150,
        unique=True,
        help_text='До 150 символов. Используются буквы, цифры и  @/./+/-/'
    )
    first_name = models.CharField(
        'Имя',
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        'email',
        max_length=254,
        unique=True
    )

    bio = models.TextField(
        'Биография',
        blank=True
    )

    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.MAX_CODE_LENGTH,
        default="0",
        blank=True

    )
    # Роль пользоватетля
    role = models.CharField(
        'Роль',
        max_length=15,
        choices=CHOICE_ROLES,
        default='user'
    )

    class Metta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]

    def __str__(self) -> str:
        return self.username
