from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.hashers import make_password
from django.utils import timezone

from .models import Client, ClientRequest, ClientUser
from .serializers import (
    ClientSignupSerializer,
    ClientRequestSerializer,
    ClientProfileSerializer,
    ClientRoleSerializer, 
    ClientUserSerializer,
    ClientUserPasswordResetSerializer
)
from .utils import authenticate_client, get_tokens_for_client
from .utils import authenticate_client_user, get_tokens_for_client_user

from .authentication import ClientJWTAuthentication, ClientUserJWTAuthentication
from .permissions import IsCompanyOwner

 
class ClientSignupAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ClientSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client = serializer.save()
        return Response(
            {"message": "Signup successful.", "client_id": client.id},
            status=status.HTTP_201_CREATED
        )

class ClientLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("company_email")
        password = request.data.get("password")
        client = authenticate_client(email, password)
        if not client:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_client(client)
        return Response({"tokens": tokens}, status=status.HTTP_200_OK)

 
class ClientRequestCreateAPIView(APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if ClientRequest.objects.filter(client=request.user).exists():
            return Response({"error": "Request already submitted"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClientRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(client=request.user, request_status="pending")
        return Response({"message": "Request submitted"}, status=status.HTTP_201_CREATED)


 
class ClientProfileAPIView(APIView):
     
    authentication_classes = [ClientJWTAuthentication, ClientUserJWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        client = request.user.client if hasattr(request.user, 'client') else request.user
        serializer = ClientProfileSerializer(client)
        return Response(serializer.data)

    def patch(self, request):
        if not hasattr(request.user, 'company_email'):
             return Response({"detail": "Only company owner can update profile"}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = ClientProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

 
class ClientUserViewSet(viewsets.ModelViewSet):
    """
    Handles List, Create, Retrieve, Update, Delete and Custom Actions for Staff.
    """
    serializer_class = ClientUserSerializer
    authentication_classes = [ClientJWTAuthentication, ClientUserJWTAuthentication]

    def get_permissions(self):
        if self.action in ['create', 'toggle_status', 'destroy']:
            return [IsCompanyOwner()]
        return [IsAuthenticated()]

    def get_queryset(self):
        # Security: Filter users belonging to the logged-in client's company
        user = self.request.user
        client_obj = user.client if hasattr(user, 'client') else user
        return ClientUser.objects.filter(client=client_obj)

    def perform_create(self, serializer):
        # Automatically link the new user to the logged-in client
        serializer.save(client=self.request.user)

    @action(detail=True, methods=['patch'], url_path='toggle-status')
    def toggle_status(self, request, pk=None):
        user = self.get_object()
        user.is_active = not user.is_active
        user.save()
        return Response({"message": f"User {'activated' if user.is_active else 'deactivated'}"})

 

class ClientRoleCreateAPIView(APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [IsCompanyOwner]

    def post(self, request):
        serializer = ClientRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

 
class ClientUserPasswordResetAPIView(APIView):
    authentication_classes = [ClientJWTAuthentication]
    permission_classes = [IsAuthenticated, IsCompanyOwner]

    def post(self, request):
        serializer = ClientUserPasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Client user password reset successfully"}, status=status.HTTP_200_OK)


class ClientUserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        identifier = request.data.get("email") # Identifier (Email)
        password = request.data.get("password")
        
        if not identifier or not password:
            return Response({"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST)

        
        user = authenticate_client_user(identifier, password)
        if not user:
            return Response({"error": "Invalid staff credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        tokens = get_tokens_for_client_user(user)
        return Response({
            "message": "Staff login successful",
            "user_details": {
                "name": user.full_name,
                "role": user.role.role_name if user.role else "No Role"
            },
            "tokens": tokens
        }, status=status.HTTP_200_OK)

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth.hashers import make_password
# from django.shortcuts import get_object_or_404

# from .models import Client, ClientRequest, ClientUser
# from .serializers import (
#     ClientSignupSerializer,
#     ClientRequestSerializer,
#     ClientProfileSerializer,
#     ClientRoleSerializer, 
#     ClientUserSerializer,
#     ClientUserPasswordResetSerializer
# )
# from .utils import authenticate_client, get_tokens_for_client
# from .authentication import ClientJWTAuthentication
# from rest_framework.permissions import IsAuthenticated, AllowAny
# from rest_framework import viewsets
# from rest_framework.decorators import action
# from rest_framework import permissions
# from .permissions import IsCompanyOwner, IsClientStaff
# from .authentication import ClientJWTAuthentication, ClientUserJWTAuthentication

# class ClientSignupAPIView(APIView):
#     permission_classes = [AllowAny]  # Public

#     def post(self, request):
#         serializer = ClientSignupSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         client = serializer.save()
#         return Response(
#             {"message": "Signup successful. You can login now.", "client_id": client.id},
#             status=status.HTTP_201_CREATED
#         )


 
# class ClientLoginAPIView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get("company_email")
#         password = request.data.get("password")
#         if not email or not password:
#             return Response(
#                 {"error": "Email and password required"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         client = authenticate_client(email, password)
#         if not client:
#             return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         tokens = get_tokens_for_client(client)
#         return Response(
#             {"message": "Login successful", "tokens": tokens}, status=status.HTTP_200_OK
#         )


 
# class ClientRequestCreateAPIView(APIView):
#     authentication_classes = [ClientJWTAuthentication]  # require login
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         client = request.user  # from JWT token

#         # prevent duplicate request
#         if ClientRequest.objects.filter(client=client).exists():
#             return Response(
#                 {"error": "Request already submitted"}, status=status.HTTP_400_BAD_REQUEST
#             )

#         serializer = ClientRequestSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(client=client, request_status="pending")

#         return Response(
#             {
#                 "message": "Client request submitted",
#                 "request_id": serializer.instance.id,
#                 "request_status": serializer.instance.request_status,
#             },
#             status=status.HTTP_201_CREATED
#         )


 
# class ClientProfileAPIView(APIView):
#     authentication_classes = [ClientJWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         client = request.user
#         serializer = ClientProfileSerializer(client)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def patch(self, request):
#         client = request.user
#         serializer = ClientProfileSerializer(client, data=request.data, partial=True)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(
#             {"message": "Profile updated successfully", "data": serializer.data},
#             status=status.HTTP_200_OK
#         )

 
# class ClientRoleCreateAPIView(APIView):
#     authentication_classes = [ClientJWTAuthentication]
#     permission_classes = [IsAuthenticated]  # Only logged-in clients

#     def post(self, request):
#         client = request.user
#         serializer = ClientRoleSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Client role created", "data": serializer.data}, status=status.HTTP_201_CREATED)

 
# class ClientUserCreateAPIView(APIView):
#     authentication_classes = [ClientJWTAuthentication, ClientUserJWTAuthentication]
#     permission_classes = [IsAuthenticated]  # Only client can create users

#     def post(self, request):
#         # Optional: enforce only certain roles can create users
#         # check_client_user_role(request.user, "admin")  # Example
#         client = request.user 
#         data = request.data
#         data["client"] = client.id 
#         serializer = ClientUserSerializer(data=data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save(password_hash=make_password(serializer.validated_data["password"]))
#         return Response({"message": "Client user created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)


 
# class ClientUserPasswordResetAPIView(APIView):
#     permission_classes = [IsAuthenticated]  # Logged-in client can reset password for its users

#     def post(self, request):
#         serializer = ClientUserPasswordResetSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"message": "Client user password reset successfully"}, status=status.HTTP_200_OK)

# # clients/views.py




# class ClientUserViewSet(viewsets.ModelViewSet):
#     queryset = ClientUser.objects.all()
#     serializer_class = ClientUserSerializer
#     authentication_classes = [ClientUserJWTAuthentication, ClientJWTAuthentication]

#     def get_permissions(self):
#         # Professional RBAC: Create/Toggle sirf Company Owner kar sake
#         if self.action in ['create', 'toggle_status', 'destroy']:
#             return [IsCompanyOwner()]
#         return [permissions.IsAuthenticated()]

#     def get_queryset(self):
#         # Security: User sirf apni hi company ke employees dekh sake
#         return ClientUser.objects.filter(client=self.request.user.client if hasattr(self.request.user, 'client') else self.request.user)

#     @action(detail=True, methods=['patch'], url_path='toggle-status')
#     def toggle_status(self, request, pk=None):
#         user = self.get_object()
#         user.is_active = not user.is_active
#         user.save()
#         status_msg = "activated" if user.is_active else "deactivated"
#         return Response({"message": f"Staff user {status_msg} successfully"})