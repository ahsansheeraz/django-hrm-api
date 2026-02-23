from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions
from .models import Administrator

class AdminJWTAuthentication(JWTAuthentication):
    """
    Custom JWTAuthentication for Administrator model
    """

    def get_user(self, validated_token):
        admin_id = validated_token.get("admin_id")
        if not admin_id:
            raise exceptions.AuthenticationFailed("Admin ID missing in token")

        try:
            admin = Administrator.objects.get(id=admin_id, is_active=True)
        except Administrator.DoesNotExist:
            raise exceptions.AuthenticationFailed("Administrator not found or inactive")

        # Add is_authenticated property to satisfy DRF
        admin.is_authenticated = True
        return admin
