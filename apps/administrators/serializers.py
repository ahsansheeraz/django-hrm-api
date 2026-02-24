from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import Administrator, AdministratorRole
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # Add custom claims
        token['admin_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['role'] = 'administrator'
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Add custom response data
        data.update({
            'admin_id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'role': 'administrator',
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
        })
        
        return data

# --- Existing Serializers (Jo aapne pehle share kiye) ---

class AdministratorRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdministratorRole
        fields = ("role_id", "role_name", "adminsistrators_roles_status", "created_at", "updated_at")
        read_only_fields = ("role_id", "created_at", "updated_at")

class AdministratorSerializer(serializers.ModelSerializer):
    # Professional touch: Role ka naam bhi sath dikhayen ge
    role_name = serializers.ReadOnlyField(source='role.role_name')
    
    class Meta:
        model = Administrator
        fields = (
            "id", "username", "email", "first_name", "mid_name", "last_name", 
            "phone", "designation", "photo", "role", "role_name", 
            "is_active", "status", "last_time", "created_at", "updated_at"
        )
        read_only_fields = ("id", "created_at", "updated_at", "last_time")

class AdminLoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)


 
# --- New Professional Serializers ---

class AdministratorCreateSerializer(serializers.ModelSerializer):
    """
    Naya Admin ya Manager create karne ke liye.
    Password hashing logic yahan handle ho rahi hai.
    """
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = Administrator
        fields = (
            "username", "email", "password", "first_name", 
            "last_name", "role", "designation"
        )

    def create(self, validated_data):
        # Password ko hash karna zaroori hai
        validated_data['password_hash'] = make_password(validated_data.pop('password'))
        return super().create(validated_data)


class AdministratorProfileUpdateSerializer(serializers.ModelSerializer):
    """
    User khud apni profile update karne ke liye use karega.
    Ismein role ya is_active change karne ki permission nahi hogi.
    """
    class Meta:
        model = Administrator
        fields = (
            "first_name", "mid_name", "last_name", 
            "phone", "designation", "photo"
        )


class PasswordChangeSerializer(serializers.Serializer):
    """
    Password change logic ke liye validation.
    """
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError({"password": "New passwords do not match."})
        return data