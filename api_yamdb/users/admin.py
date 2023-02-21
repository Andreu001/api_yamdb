from django.contrib import admin
from users.models import User


class UserAdmin(admin.ModelAdmin):
    """Кастомный пользователь в админки"""
    list_display = (
        'pk',
        'username',
        'role',
        'first_name',
        'last_name',
        'email'
    )
    search_fields = ('username',)


admin.site.register(User, UserAdmin)
