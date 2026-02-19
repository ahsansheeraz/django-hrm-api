from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.contrib.auth.hashers import check_password

from .models import Administrator


def get_tokens_for_administrator(admin):
    """
    Generate JWT refresh and access tokens for Administrator
    with custom claims: admin_id and role
    """
    refresh = RefreshToken.for_user(admin)  # link with admin object
    refresh["admin_id"] = admin.id
    refresh["role"] = "administrator"

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def authenticate_admin_with_email_or_username(identifier, password):
    """
    Authenticate Administrator by email or username
    """
    try:
        admin = Administrator.objects.get(
            Q(email=identifier) | Q(username=identifier),
            is_active=True
        )
    except Administrator.DoesNotExist:
        return None

    if check_password(password, admin.password_hash):
        return admin

    return None

