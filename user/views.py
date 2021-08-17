
from rest_framework import generics,  status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken, Token, TokenError
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from django.conf import settings
from user.models import MyUser
from django.conf import settings
from .serializers import (ChangePasswordSerializer,
                          CookieTokenRefreshSerializer, LoginSerializer,
                          RegisterSerializer)
import jwt
# Create your views here.


class RegisterView(GenericAPIView):
    """
    POST api/user/register/
    """
    serializer_class = RegisterSerializer
    queryset = MyUser.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        user = request.data
        serializer = self.serializer_class(data=user)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


# class MyObtainTokenPairView(TokenObtainPairView):
#     """
#     POST api/user/login
#     """
#     permission_classes = [AllowAny]
#     serializer_class = MyTokenObtainPairSerializer


class LoginView(APIView):
    """
    POST api/user/login/
    """
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        response = Response(data, status=status.HTTP_200_OK)

        cookie_max_age = 3600 * 24 * 14  # 14 days

        response.set_cookie(
            'refresh_token', data['refresh'], max_age=cookie_max_age, httponly=True)
        del response.data['refresh']
        response.set_cookie('access_token', data['access'], httponly=True)
        return response


class CookieTokenRefreshView(TokenRefreshView):
    """
    POST api/user/login/refresh/

    """
    serializer_class = CookieTokenRefreshSerializer

    def finalize_response(self, request, response, *args, **kwargs):
        if response.data.get('refresh'):
            cookie_max_age = 3600 * 24 * 14  # 14 days
            response.set_cookie(
                'refresh_token', response.data['refresh'], max_age=cookie_max_age, httponly=True)
            del response.data['refresh']
        return super().finalize_response(request, response, *args, **kwargs)


class ChangePasswordView(generics.UpdateAPIView):
    queryset = MyUser.objects.all()
    permission_classes = (IsAuthenticated)
    serializer_class = ChangePasswordSerializer


class LogoutView(APIView):
    """
    POST api/user/logout/
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.COOKIES['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response('success', status=status.HTTP_205_RESET_CONTENT)
        except TokenError:
            return Response('fail', status=status.HTTP_400_BAD_REQUEST)


# class LogoutAPIView(generics.GenericAPIView):
#     serializer_class = LogoutSerializer

#     permission_classes = (permissions.IsAuthenticated,)

#     def post(self, request):

#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         return Response(status=status.HTTP_204_NO_CONTENT)
