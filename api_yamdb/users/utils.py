from hashlib import sha1
from random import choice
from string import ascii_lowercase
from django.conf import settings
from django.core.mail import send_mail
import re
from rest_framework.exceptions import ValidationError


def username_validate(name):
    """"""
    regex = re.compile(r'^[\w.@+-]+')
    if not regex.match(name):
        raise ValidationError(
                f'Не допустимые символы в имени',
                f'Имя может содержать только буквы, цифры и',
                f'символы @/./+/-/_ '
            )


def get_unique_confirmation_code():
    """Функция генерации кода подтверждения для отправки пользователю"""
    code = "".join(
        [
            choice(ascii_lowercase) for _ in range(settings.MAX_CODE_LENGTH)
        ]
    )
    return sha1(code.encode()).hexdigest()[:settings.MAX_CODE_LENGTH]


def sent_email_with_confirmation_code(to_email, code):
    """Отправка сообщения пользователю с кодом подтверждения"""
    subject = ''
    message = (
        f'Ваш код подтверждения для регистрации: {code}'
        f'Вам необходимо отправить запрос /api/v1/auth/token/'
        f'В запросе передайте username и confirmation_code'
    )

    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [to_email])
