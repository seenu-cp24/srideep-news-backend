from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrReadOnly(BasePermission):
    """
    - Public: READ only
    - Admin (is_staff or is_superuser): FULL access
    """

    def has_permission(self, request, view):

        # Public read-only access
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Admin users only for write
        return request.user.is_staff or request.user.is_superuser


class IsAuthenticatedOrReadOnly(BasePermission):
    """
    - Public: READ only
    - Authenticated users: CREATE only (no update/delete)
    """

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated
