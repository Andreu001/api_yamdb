from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

CHOICE_ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin')
)


class User(AbstractUser):
    """Кастомная модель пользователя унаследованная от AbstractUser
    для расширения атрибутов пользователя"""
    bio = models.TextField(
        'Биография',
        blank=True,
    )
    # Код подтверждения
    confirmation_code = models.CharField(
        'Код подтверждения',
        max_length=settings.MAX_CODE_LENGTH,
        blank=True,
        null=True
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
