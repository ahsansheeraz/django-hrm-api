from rest_framework.permissions import BasePermission
from apps.accounts.models import Administrator

class IsAdministrator(BasePermission):
    """
    Allow access only to active Administrators
    """

    def has_permission(self, request, view):
        user = getattr(request, "user", None)
        if not user:
            return False

        if not isinstance(user, Administrator):
            return False

        if not user.is_active:
            return False

        # Add is_authenticated property to avoid DRF errors
        user.is_authenticated = True
        return True
