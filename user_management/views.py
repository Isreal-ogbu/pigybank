import datetime
import uuid

from decouple import config
from django.conf import settings
from django.contrib.auth import get_user_model, logout
from django.contrib.auth import login as django_login, logout as django_logout
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from knox.views import LoginView as KnoxLogin, LogoutView as KnoxLogout, LogoutAllView
from rest_framework.views import APIView

from .serializers import UserSerializer, ReadUserSerializer, LoginSerializer, EmailVerificationSerializer, \
    SetPasswordSerializer, Emailserialisers
from user_management.models import EmailVerification
from utils.util import ResponseModelViewSet, error_handler, ResponseAPIView
from django.utils.translation import gettext_lazy as _

from utils.verify import regular

User = get_user_model()


class UserViewSet(ResponseModelViewSet):
    serializer_class = ReadUserSerializer
    permission_classes = [IsAuthenticated, ]
    pagination_class = None

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)


class UsersSerializerViewSet(ResponseModelViewSet):
    """For administrative use only"""
    queryset = User.objects.all()
    permission_classes = [IsAdminUser, ]
    serializer_class = UserSerializer
    pagination_class = None


class RegistrationViewSet(ResponseModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get', 'post']
    permission_classes = [AllowAny]

    def get_queryset(self):
        return super().get_queryset().none()

    def list(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)


class LoginViewSet(GenericAPIView, KnoxLogin):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data['user']
            django_login(request, user)
            response = super().post(request, format=None)
            if response.status_code != 200:
                raise Exception(response.data['error'])
            response = Response({
                "status": 'success',
                "data": response.data,
                "message": 'success'
            }, status=status.HTTP_200_OK)
            return response

        except Exception as e:
            return Response({
                "status": 'failed',
                "data": [],
                "message": error_handler(e)
            }, status=status.HTTP_401_UNAUTHORIZED)

    def get(self, request, format=None):
        return Response(status=status.HTTP_200_OK)


class LogoutViewSet(KnoxLogout):
    permission_classes = [IsAuthenticated, ]

    def logout(self, request):
        logout(request)
        if getattr(settings, 'REST_SESSION_LOGIN', True):
            django_logout(request)

        response = Response(
            {'detail': _('Successfully logged out.')},
            status=status.HTTP_200_OK,
        )

        return response

    def post(self, request, *args, **kwargs):
        super().post(request, format=None)
        return self.logout(request)


class EmailVerificationViewSet(ResponseAPIView):
    serializer_class = EmailVerificationSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            token = serializer.validated_data['token']
            user_data = EmailVerification.objects.get(token=token)
        except Exception as e:
            msg = error_handler(e)
            return Response({
                "status": 'Failed',
                "data": [],
                "message": msg
            }, status=status.HTTP_400_BAD_REQUEST)
        if user_data.date_updated + datetime.timedelta(minutes=30) > datetime.datetime.now(datetime.timezone.utc):
            user_data.is_verified = True
            user_data.save()
            return Response({
                "status": 'Success',
                "data": UserSerializer(user_data.user).data,
                "message": 'Email Verification Successful'
            }, status=status.HTTP_200_OK)
        else:
            msg = "Verification link expired. Request new verification link"
            return Response({
                "status": 'Failed',
                "data": [],
                "message": msg
            }, status=status.HTTP_205_RESET_CONTENT)


class ReverificationViewSet(ResponseAPIView):
    serializer_class = Emailserialisers
    http_method_names = ['post']
    permission_classes = ()

    def post(self, request, format=None):
        serailizer = self.get_serializer(data=request.data)
        serailizer.is_valid(raise_exception=True)
        try:
            user = User.objects.get(email__iexact=serailizer.validated_data['email'])
        except Exception as e:
            msg = error_handler('User does not exist')
            return Response({
                "status": 'Failed',
                "data": [],
                "message": msg
            }, status=status.HTTP_400_BAD_REQUEST)
        try:
            user_data = EmailVerification.objects.get(user=user)
        except Exception as e:
            msg = error_handler("You are a super admin. No verification record")
            return Response({
                "status": 'Failed',
                "data": [],
                "message": msg
            }, status=status.HTTP_400_BAD_REQUEST)

        generate = uuid.uuid4()
        user_data.date_updated = datetime.datetime.now()
        user_data.token = generate
        user_data.is_verified = False
        user_data.save()
        regular(user_data.user, generate)
        return Response(self.response_format, status=status.HTTP_200_OK)


class SetPasswordView(ResponseAPIView):
    serializer_class = SetPasswordSerializer
    http_method_names = ['post']

    @transaction.atomic
    def post(self, request, user_id, format=None):
        try:
            obj = User.objects.get(id=user_id)
            """Configured the default password so it will not be exposed cause it is saving as blank"""
            if obj.password != config("DEFAULT_PASSWORD"): raise Exception('Password has already been set')
            serializer = self.get_serializer(data=request.data, instance=obj)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception as e:
            e = error_handler(e)
            return Response(
                {
                    "status": 'Success',
                    "data": e,
                    "message": 'Success'
                }, status=status.HTTP_200_OK
            )

        return Response(
            {
                "status": 'Success',
                "data": serializer.data,
                "message": 'Success'
            }, status=status.HTTP_200_OK
        )

    def get(self, request, uuid, format=None):
        return Response(status=status.HTTP_200_OK)
