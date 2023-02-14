from hashlib import sha1
from random import choice
from string import ascii_lowercase
from django.conf import settings
from django.core.mail import send_mail


def get_unique_confirmation_code():
    """Функция генерации кода подтверждения для отправки пользователю"""
    code = "".join(
        [
            choice(ascii_lowercase) for _ in range(settings.MAX_CODE_LENGTH)
        ]
    )
    return sha1(code.encode()).hexdigest()[:settings.MAX_CODE_LENGTH]


def sent_email_with_confirmation_code():
    """Отправка сообщения пользователю с кодом подтверждения"""

    pass
