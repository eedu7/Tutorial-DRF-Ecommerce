from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.serializers import (
    UserRegistrationSerializer,
    UserProfileSerializer,
)


# Token Generation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# Create your views here.
class UserRegistrationAPIView(GenericAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response(
            {"token": token, "user": serializer.data}, status=status.HTTP_201_CREATED
        )


class UserLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # serializer = UserLoginSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # username = serializer.data.get("username")
        # password = serializer.data.get("password")
        username = self.request.data.get("username")
        password = self.request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            token = get_tokens_for_user(user)
            return Response(
                {"token": token, "msg": "Login Success"}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"errors": {"non_field_errors": ["Email or Password is not Valid"]}},
                status=status.HTTP_404_NOT_FOUND,
            )


class UserProfileAPIView(GenericAPIView):
    serializer_class = UserProfileSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
