from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
from django.contrib.auth.hashers import check_password

from apps.accounts.models import Administrator, ClientUser


def get_tokens_for_administrator(admin):
    """
    Generate JWT refresh and access tokens for Administrator
    with custom claims: admin_id and role
    """
    refresh = RefreshToken.for_user(admin)  # link with object
    refresh["admin_id"] = admin.id
    refresh["role"] = "administrator"

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


def get_tokens_for_client_user(client_user):
    """
    Generate JWT tokens for ClientUser
    """
    refresh = RefreshToken.for_user(client_user)
    refresh["client_user_id"] = client_user.id
    refresh["role"] = "client_user"

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


def authenticate_client_user_with_email_or_username(identifier, password):
    """
    Authenticate ClientUser by email
    """
    try:
        user = ClientUser.objects.get(
            email=identifier,
            is_active=True
        )
    except ClientUser.DoesNotExist:
        return None

    if check_password(password, user.password_hash):
        return user

    return None
