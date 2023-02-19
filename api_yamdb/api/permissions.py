from rest_framework import permissions


class IsAdminUserOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user  # было request.user.is_admin
        return False

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return(
            request.user.is_authenticated and(
                request.user.is_admin or
                request.user.is_staff or
                request.user.is_superuser
            )
        )

