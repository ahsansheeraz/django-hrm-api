from rest_framework import serializers
from .models import (
    Administrator,
    AdministratorRole,
    ClientRequest,
    Client,
    ClientRole,
    ClientUser
)
 

class AdministratorRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorRole
        fields = (
            "role_id",
            "role_name",
            "adminsistrators_roles_status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("role_id", "created_at", "updated_at")


class AdministratorSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True)

    class Meta:
        model = Administrator
        fields = (
            "id",
            "username",
            "email",
            "password_hash",
            "first_name",
            "mid_name",
            "last_name",
            "phone",
            "designation",
            "photo",
            "role",
            "is_active",
            "status",
            "last_time",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "created_at", "updated_at")


class AdminLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)




class ClientRequestSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # new field for input

    class Meta:
        model = ClientRequest
        fields = (
            "id",
            "company_email",
            "company_phone",
            "company_name",
            "company_website",
            "industry_type",
            "company_size",
            "request_status",
            "approved_by_administrator",
            "approved_at",
            "password",       # add here
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "approved_at", "created_at", "updated_at")

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        if password:
            validated_data["password_hash"] = make_password(password)
        return super().create(validated_data)


class ClientSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True)

    class Meta:
        model = Client
        fields = (
            "id",
            "request",
            "password_hash",
            "company_logo",
            "is_verified",
            "is_active",
            "last_login",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "last_login", "created_at", "updated_at")


class ClientRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientRole
        fields = (
            "role_id",
            "role_name",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("role_id", "created_at", "updated_at")


class ClientUserSerializer(serializers.ModelSerializer):
    password_hash = serializers.CharField(write_only=True)

    class Meta:
        model = ClientUser
        fields = (
            "id",
            "client",
            "role",
            "email",
            "password_hash",
            "full_name",
            "phone",
            "is_active",
            "last_login",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "last_login", "created_at", "updated_at")


class ClientUserLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)
