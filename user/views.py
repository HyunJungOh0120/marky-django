from user.models import MyUser
from django.shortcuts import render


from rest_framework import status
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
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


class LoginAPIView(GenericAPIView):
    queryset = MyUser.objects.all()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
