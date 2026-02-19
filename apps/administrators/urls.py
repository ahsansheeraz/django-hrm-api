from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AdministratorLoginAPIView, 
    ClientRequestListAPIView, 
    ApproveClientRequestAPIView,
    AdministratorManagementViewSet,
    AdminProfileAPIView,
    AdminPasswordChangeAPIView,
    AdminDashboardStatsAPIView,
     
)

# Router ViewSets ke liye use hota hai (CRUD operations automatically handle karta hai)
router = DefaultRouter()
router.register(r'management', AdministratorManagementViewSet, basename='admin-management')

urlpatterns = [
    # Existing URLs
    path("login/", AdministratorLoginAPIView.as_view(), name="admin-login"),
    path("client-requests/", ClientRequestListAPIView.as_view(), name="admin-client-request-list"),
    path("client-requests/<int:request_id>/approve/", ApproveClientRequestAPIView.as_view(), name="admin-approve-client-request"),

    # New URLs
    path("profile/", AdminProfileAPIView.as_view(), name="admin-profile"),
    path("change-password/", AdminPasswordChangeAPIView.as_view(), name="admin-change-password"),
    path("dashboard-stats/", AdminDashboardStatsAPIView.as_view(), name="admin-dashboard-stats"),
     # ViewSet URLs (management/ se start honge)
    path("", include(router.urls)),
]