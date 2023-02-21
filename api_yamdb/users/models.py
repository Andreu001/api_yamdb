from django.contrib.auth.models import AbstractUser
from django.db import models

USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

CHOICE_ROLES = [
    (USER, USER),
    (ADMIN, ADMIN),
    (MODERATOR, MODERATOR),
]


class User(AbstractUser):
    """Кастомная модель пользователя унаследованная от AbstractUser
    для расширения атрибутов пользователя"""

    username = models.CharField(
        verbose_name='Пользователь',
        max_length=150,
        unique=True,
        help_text='До 150 символов. Используются буквы, цифры и  @/./+/-/'
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=150,
        blank=True
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=150,
        blank=True
    )

    email = models.EmailField(
        verbose_name='email',
        max_length=254,
        unique=True
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=CHOICE_ROLES,
        default='user'
    )

    @property
    def is_user(self):
        return self.role == USER

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username', 'email'],
                                    name='unique_user')
        ]

    def __str__(self) -> str:
        return self.username
