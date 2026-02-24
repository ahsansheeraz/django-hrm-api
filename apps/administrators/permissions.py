from rest_framework.permissions import BasePermission
from .models import Administrator

class IsAdministrator(BasePermission):
    """
    Allow access only to authenticated administrators
    (JWT based)
    """

    def has_permission(self, request, view):
        if not hasattr(request, "auth") or not request.auth:
            return False

        if request.auth.get("role") != "administrator":
            return False

        admin_id = request.auth.get("admin_id")
        if not admin_id:
            return False

        return Administrator.objects.filter(
            id=admin_id,
            is_active=True
        ).exists()

