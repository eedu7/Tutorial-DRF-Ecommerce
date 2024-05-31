from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.views import UserRegistrationAPIView, UserLoginAPIView, UserProfileAPIView, UserPasswordChangeAPIView

urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="obtain-token"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("verify/", TokenVerifyView.as_view(), name="verify-token"),
    path(
        "user-registration/",
        UserRegistrationAPIView.as_view(),
        name="user-registration",
    ),
    path("profile/", UserProfileAPIView.as_view(), name="user-profile"),
    path("login/", UserLoginAPIView.as_view(), name="user-login"),
    path("profile/change-password/", UserPasswordChangeAPIView.as_view(), name="user-change-password"),
]
