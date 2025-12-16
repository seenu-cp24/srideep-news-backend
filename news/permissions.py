from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminEditorReporter(BasePermission):
    """
    Role-based permission:
    - Admin: full access
    - Editor: create & update
    - Reporter: create drafts only
    - Public: read-only
    """

    def has_permission(self, request, view):

        # Public read access
        if request.method in SAFE_METHODS:
            return True

        # Must be authenticated
        if not request.user or not request.user.is_authenticated:
            return False

        # Must have author profile
        if not hasattr(request.user, "author_profile"):
            return False

        role = request.user.author_profile.role

        return role in ["admin", "editor", "reporter"]
