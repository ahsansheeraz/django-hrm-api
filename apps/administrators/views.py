from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth.hashers import check_password, make_password
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Administrator
from .serializers import (
    AdminLoginSerializer, AdministratorSerializer, 
    AdministratorCreateSerializer, AdministratorProfileUpdateSerializer,
    PasswordChangeSerializer
)
from .utils import authenticate_admin_with_email_or_username, get_tokens_for_administrator
from .permissions import IsAdministrator
from .authentication import AdminJWTAuthentication

from apps.clients.models import ClientRequest 
from apps.clients.serializers import ClientRequestSerializer

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

 
# --- Existing Views ---
class AdministratorLoginAPIView(APIView):
     permission_classes = [] 

     def post(self, request):
         identifier = request.data.get("email_or_username")
         password = request.data.get("password")
         user = authenticate_admin_with_email_or_username(identifier, password)
         if not user:
             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
         # Last login update yahan professional tareeqa hai
         user.last_time = timezone.now()
         user.save()
        
         tokens = get_tokens_for_administrator(user)
         return Response({"message": "Admin login successful", "tokens": tokens})
# In views.py, add these missing classes:

class ClientRequestListAPIView(APIView):
    permission_classes = [IsAdministrator]
    authentication_classes = [AdminJWTAuthentication]

    def get(self, request):
        
        requests = ClientRequest.objects.all().order_by("-created_at")
        serializer = ClientRequestSerializer(requests, many=True)
        return Response(serializer.data)


class ApproveClientRequestAPIView(APIView):
    permission_classes = [IsAdministrator]
    authentication_classes = [AdminJWTAuthentication]

    def post(self, request, request_id):
        client_request = get_object_or_404(ClientRequest, id=request_id)

        # Professional Improvement: query ki bajaye direct request.user use karein
        client_request.request_status = "approved"
        client_request.approved_by_administrator = request.user 
        client_request.approved_at = timezone.now()
        client_request.save()

        return Response(
            {"message": "Client request approved successfully"},
            status=status.HTTP_200_OK
        )
# --- New User Management ViewSet ---
class AdministratorManagementViewSet(viewsets.ModelViewSet):
    """
    Admin/Manager CRUD aur Status Toggle ke liye.
    URL endpoints: list, create, retrieve, partial_update
    """
    queryset = Administrator.objects.all().order_by("-created_at")
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAdministrator]

    def get_serializer_class(self):
        if self.action == 'create':
            return AdministratorCreateSerializer
        return AdministratorSerializer

    @action(detail=True, methods=['patch'], url_path='toggle-status')
    def toggle_status(self, request, pk=None):
        """Custom endpoint: admin/id/toggle-status/"""
        admin_user = self.get_object()
        admin_user.is_active = not admin_user.is_active
        admin_user.save()
        status_msg = "activated" if admin_user.is_active else "deactivated"
        return Response({"message": f"User {status_msg} successfully"})

# --- Profile & Security Views ---
class AdminProfileAPIView(APIView):
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request):
        serializer = AdministratorSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = AdministratorProfileUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Profile updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminPasswordChangeAPIView(APIView):
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAdministrator]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not check_password(serializer.validated_data['old_password'], user.password_hash):
                return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
            
            user.password_hash = make_password(serializer.validated_data['new_password'])
            user.save()
            return Response({"message": "Password changed successfully"})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# --- Dashboard Stats ---
class AdminDashboardStatsAPIView(APIView):
    authentication_classes = [AdminJWTAuthentication]
    permission_classes = [IsAdministrator]

    def get(self, request):
        data = {
            "total_admins": Administrator.objects.count(),
            "active_admins": Administrator.objects.filter(is_active=True).count(),
            "pending_client_requests": ClientRequest.objects.filter(request_status="pending").count(),
        }
        return Response(data)
    

