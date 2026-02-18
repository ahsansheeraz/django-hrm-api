from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from apps.accounts.utils import (
    authenticate_client_user_with_email_or_username,
    get_tokens_for_client_user
)

from apps.accounts.models import (
    ClientRequest,
    Client,
    ClientUser
)
from apps.accounts.serializers import (
    ClientRequestSerializer,
    ClientUserSerializer,
    ClientUserLoginSerializer
)




class ClientRequestCreateAPIView(APIView):
    permission_classes = []  # public

    def post(self, request):
        serializer = ClientRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request_status="pending")

        return Response(
            {"message": "Client request submitted"},
            status=status.HTTP_201_CREATED
        )



 

class ClientProfileSetupAPIView(APIView):
    def post(self, request):
        request_id = request.data.get("request_id")

        try:
            client_request = ClientRequest.objects.get(
                id=request_id,
                request_status="approved"
            )
        except ClientRequest.DoesNotExist:
            return Response(
                {"detail": "Invalid or unapproved request"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Use password_hash from the request
        client = Client.objects.create(
            request=client_request,
            password_hash=client_request.password_hash,
            is_verified=True,
            is_active=True
        )

        return Response(
            {
                "message": "Client profile created successfully",
                "client_id": client.id
            },
            status=status.HTTP_201_CREATED
        )



class ClientUserCreateAPIView(APIView):
    def post(self, request):
        serializer = ClientUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(
            password_hash=make_password(
                serializer.validated_data["password_hash"]
            )
        )

        return Response(
            {"message": "Client user created successfully"},
            status=status.HTTP_201_CREATED
        )



class ClientLoginAPIView(APIView):
    permission_classes = []

    def post(self, request):
        identifier = request.data.get("email_or_username")
        password = request.data.get("password")

        client_user = authenticate_client_user_with_email_or_username(
            identifier, password
        )

        if not client_user:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        tokens = get_tokens_for_client_user(client_user)
        return Response({
            "message": "Client login successful",
            "tokens": tokens
        })
