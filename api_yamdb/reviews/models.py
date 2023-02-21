from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User

from .validators import validate_year


class Category(models.Model):
    name = models.CharField(
        'имя категории',
        max_length=256
    )
    slug = models.SlugField(
        'слаг категории',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name} {self.name}'


class Genre(models.Model):
    name = models.CharField(
        'имя жанра',
        max_length=256
    )
    slug = models.SlugField(
        'cлаг жанра',
        unique=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return f'{self.name} {self.name}'


class Title(models.Model):
    name = models.CharField(
        'название произведения',
        max_length=256,
        db_index=True
    )
    year = models.IntegerField(
        'год',
        validators=(validate_year, )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='категория',
        null=True,
        blank=True
    )
    description = models.TextField(
        'описание',
        max_length=255,
        null=True,
        blank=True
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='жанр'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name


class Review (models.Model):
    """Класс Отзыв. Пользователь пишет отзывы на произведения.
    Отзыв должен быть привязан к конкретному произведению,
    на которое написан отзыв"""
    title = models.ForeignKey(
        Title,
        blank=True,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Отзыв',
    )
    text = models.TextField("Здесь должен быть отзыв", unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    score = models.IntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text

    class Meta:
        ordering = ('pub_date',)
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['title', 'author'],
            ),
        ]


class Comment(models.Model):
    """Класс Комментарии. Здесь будет описание комментариев пользователей
    к отзывам. Комментарии должны быть привязаны к конкретному отзыву."""
    review = models.ForeignKey(
        Review,
        blank=True,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)

# Create your models here.
