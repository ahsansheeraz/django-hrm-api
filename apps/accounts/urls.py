from django.urls import path

from apps.accounts.views.administrator_views import (
    AdministratorLoginAPIView,
    ClientRequestListAPIView,
    ApproveClientRequestAPIView
)

from apps.accounts.views.client_views import (
    ClientRequestCreateAPIView,
    ClientProfileSetupAPIView,
    ClientUserCreateAPIView,
    ClientLoginAPIView
)

urlpatterns = [

    # -------------------------
    # Administrator APIs
    # -------------------------

    path(
        "admin/login/",
        AdministratorLoginAPIView.as_view(),
        name="admin-login"
    ),

    path(
        "admin/client-requests/",
        ClientRequestListAPIView.as_view(),
        name="admin-client-request-list"
    ),

    path(
        "admin/client-requests/<int:request_id>/approve/",
        ApproveClientRequestAPIView.as_view(),
        name="admin-approve-client-request"
    ),

    # -------------------------
    # Client APIs
    # -------------------------

    path(
        "client/request/",
        ClientRequestCreateAPIView.as_view(),
        name="client-request-create"
    ),

    path(
        "client/setup-profile/",
        ClientProfileSetupAPIView.as_view(),
        name="client-profile-setup"
    ),

    path(
        "client/users/create/",
        ClientUserCreateAPIView.as_view(),
        name="client-user-create"
    ),

    
    path("client/login/", ClientLoginAPIView.as_view()),
    
]
