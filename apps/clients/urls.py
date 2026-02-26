from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (
    ClientSignupAPIView,
    ClientLoginAPIView,
    ClientRequestCreateAPIView,
    ClientProfileAPIView,
    ClientRoleCreateAPIView,
    ClientUserPasswordResetAPIView,
    ClientUserViewSet,
    ClientUserLoginAPIView
)

# Router setup for ViewSets
router = DefaultRouter()
router.register(r'users', ClientUserViewSet, basename='client-users')

urlpatterns = [
    # Auth Endpoints
    path("signup/", ClientSignupAPIView.as_view(), name="client-signup"),
    path("login/", ClientLoginAPIView.as_view(), name="client-login"),
    
    # Onboarding & Profile
    path("request/", ClientRequestCreateAPIView.as_view(), name="client-request"),
    path("profile/", ClientProfileAPIView.as_view(), name="client-profile"),
    
    path("role/create/", ClientRoleCreateAPIView.as_view(), name="client-role-create"),
    path("client-user/login/", ClientUserLoginAPIView.as_view(), name="client-user-login"),
    path("client-user/password-reset/", ClientUserPasswordResetAPIView.as_view(), name="client-user-password-reset"),
    
    # Router URLs ( automatic /users/ list aur /users/ create)
    path('', include(router.urls)),
]