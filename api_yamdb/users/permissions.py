from rest_framework import permissions


class IsOwner(permissions.BasePermission):

    """Проверка разрешения изменений объекта - владелец ли"""

    def has_object_permission(self, request, view, obj):
        if obj.username == request.user:
            return True
        return False


class IsAdminOrSuperAdmin(permissions.BasePermission):

    """Права админа или суперпользователя"""

    def has_permission(self, request, view):
        return bool(request.user.role == 'admin' or request.user.is_superuser)
