from rest_framework.permissions import IsAuthenticated, IsAdminUser

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
ADMIN_METHODS = ('GET', 'HEAD', 'OPTIONS', 'POST', 'PUT')


class SuperAdminPermission(IsAdminUser):
    def has_permission(self, request, view):
        return bool(request.method in ADMIN_METHODS and request.user and request.user.is_staff and request.user.is_superuser and request.user.is_active)


class AdminUserPermission(IsAdminUser):
    def has_permission(self, request, view):
        return bool(
            request.method in ADMIN_METHODS and request.user and
            request.user.is_authenticated and request.user.is_active and request.user.is_staff
        )


class AuthenticatedUserPermission(IsAuthenticated):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS and
            request.user and request.user.is_active and
            request.user.is_authenticated
        )