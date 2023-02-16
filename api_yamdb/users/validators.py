from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class UnicodeUsernameValidator(validators.RegexValidator):
    regex = r'^[\w.@+-]+'
    message = _(
                f'Не допустимые символы в имени',
                f'Имя может содержать только буквы, цифры и',
                f'символы @/./+/-/_ '
    )
    flags = 0
