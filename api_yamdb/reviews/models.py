from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Title (models.Model):
    pass


class Categories(models.Model):
    pass


class Genres(models.Model):
    pass


# Разработчик Андрей классы Отзывы и Комментарии, Рейтинг,
class Review (models.Model):
    """Класс Отзыв. Пользователь пишет отзывы на произведения.
    Отзыв должен быть привязан к конкретному произведению,
    на которое написан отзыв"""
    title = models.ForeignKey(
        Title,
        blank=True,  # поле title необязательно к заполнению (под вопросом)
        on_delete=models.CASCADE,  # удаление отзыва, при удалении произведения
        related_name='reviews',  # связь отзыв-произведение
        verbose_name='Отзыв',
    )
    text = models.TextField("Здесь должен быть отзыв", unique=True)
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор'
    )
    # Обязательно перепроверить
    score = models.IntegerField(  # подсчет рейтинга произведения(под вопросом)
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1),  # Проверка, чтоб оценка была не ниже 1.
            MaxValueValidator(10)  # Проверка, чтоб оценка была не ниже 10.
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


class Comment(models.Model):
    """Класс Комментарии. Здесь будет описание комментариев пользователей
    к отзывам. Комментарии должны быть привязаны к конкретному отзыву."""
    review = models.ForeignKey(
        Review,
        blank=True,
        on_delete=models.CASCADE,  # удаление комментов, при удалении отзыва
        related_name='comments',  # связь коммент-отзыв
        verbose_name='Отзыв',
    )
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',  # связь юзер коммент
        verbose_name='Пользователь',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        ordering = ('pub_date',)

    def __str__(self):
        return self.text


# Модель, возможно лишняя
# Так же есть возможность pip install django-star-rating
class Raiting(models.Model):
    """Рейтинг произведений. Здесь пользователь сможет ставить рейтинг
    произведениям от 1 до 10"""
    author = models.ForeignKey(
        User,
        blank=True,  # поле title необязательно к заполнению
        null=True,
        on_delete=models.CASCADE,
        related_name='raitings',  # связь юзер-рейтинг
        verbose_name='Пользователь',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,  # удаление рейтинга, при удалении произведен
        related_name='raitings',  # связь рейтинг-произведение
    )
    value = models.SmallIntegerField(verbose_name='Оценка')

    def __str__(self):
        return self.author

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги'
