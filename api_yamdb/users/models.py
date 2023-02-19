from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class UserRole(models.TextChoices):
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

   
class UserManagerYaMDB(UserManager):
    def create_superuser(self, username, email=None,
                         password=None, **extra_fields):
        extra_fields.setdefault('role', UserRole.ADMIN)
        return super().create_superuser(username, email,
                                        password, **extra_fields)


class User(AbstractUser):
    """Кастомная модель пользователя унаследованная от AbstractUser
    для расширения атрибутов пользователя"""
    users = UserManagerYaMDB()
    email = models.EmailField(
        verbose_name='E-mail',
        max_length=254,
        unique=True
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True
    )

    confirmation_code = models.CharField(
        verbose_name='Код подтверждения',
        max_length=20,
        blank=True

    )
    # Роль пользователя
    role = models.CharField(
        max_length=15,
        choices=UserRole.choices,
        default=UserRole.USER,
        verbose_name='Роль',
    )

    @property
    def is_admin(self):
        return (
                self.role == UserRole.ADMIN
                or self.is_staff
                or self.is_superuser
        )

    @property
    def is_moderator(self):
        return self.role == UserRole.MODERATOR

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
