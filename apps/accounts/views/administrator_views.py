from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from apps.accounts.permissions import IsAdministrator
from apps.accounts.authentication import AdminJWTAuthentication
from apps.accounts.utils import (
    authenticate_admin_with_email_or_username,
    get_tokens_for_administrator
)
from apps.accounts.models import Administrator, ClientRequest
from apps.accounts.serializers import ClientRequestSerializer


class AdministratorLoginAPIView(APIView):
    """
    Admin login endpoint
    """
    permission_classes = []

    def post(self, request):
        identifier = request.data.get("email_or_username")
        password = request.data.get("password")

        if not identifier or not password:
            return Response({"error": "Email/username and password required"}, status=400)

        admin = authenticate_admin_with_email_or_username(identifier, password)
        if not admin:
            return Response({"error": "Invalid credentials"}, status=401)

        tokens = get_tokens_for_administrator(admin)

        return Response({
            "message": "Admin login successful",
            "tokens": tokens
        }, status=200)


class ClientRequestListAPIView(APIView):
    """
    List all client requests (Admin only)
    """
    permission_classes = [IsAdministrator]
    authentication_classes = [AdminJWTAuthentication]

    def get(self, request):
        requests = ClientRequest.objects.all().order_by("-created_at")
        serializer = ClientRequestSerializer(requests, many=True)
        return Response(serializer.data, status=200)


class ApproveClientRequestAPIView(APIView):
    """
    Approve a client request by admin
    """
    permission_classes = [IsAdministrator]
    authentication_classes = [AdminJWTAuthentication]

    def post(self, request, request_id):
        client_request = get_object_or_404(ClientRequest, id=request_id)

        # request.user is guaranteed to be Administrator
        administrator = request.user

        client_request.request_status = "approved"
        client_request.approved_by_administrator = administrator
        client_request.approved_at = timezone.now()
        client_request.save()

        return Response(
            {"message": "Client request approved successfully"},
            status=status.HTTP_200_OK
        )
