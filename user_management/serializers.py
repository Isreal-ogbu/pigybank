import re

from rest_framework import serializers
from django.db import transaction
from rest_framework.exceptions import ValidationError
from django.contrib.auth import authenticate, get_user_model
from django.utils.translation import gettext_lazy as _

from user_management.models import EmailVerification
from utils.verify import regular

User = get_user_model()


def check_email(value):
    # if value.find('gmail.com') != -1:
    #     raise ValidationError('email is not a business email')
    if value.find('yahoo.com') != -1:
        raise ValidationError('email is not a business email')


class UserSerializer(serializers.ModelSerializer):
    @transaction.atomic
    def create(self, validated_data):
        validated_data['username'] = validated_data.get('email')
        user = super().create(validated_data)
        user_obj = EmailVerification.objects.create(user=user)
        token = user_obj.token
        regular(user, token)
        return user

    def validate_email(self, value):
        value = value.lower()
        check_email(value)
        return value

    class Meta:
        model = User
        exclude = ['password']
        read_only_fields = ['date_joined', 'groups', 'user_permissions', 'last_login', 'is_staff', 'is_active',
                            'username', 'is_superuser']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_email(self, email, password):

        if email and password:
            user = self.authenticate(email=email.lower(), password=password)
        else:
            msg = _('Must include "email" and "password".')

            raise Exception(msg)

        return user

    def get_auth_user_using_orm(self, email, password):
        if email:
            try:
                user = User.objects.get(email__iexact=email.lower())
            except User.DoesNotExist:
                user = None

            if user is not None:
                return self.authenticate(email=email.lower(), password=password)

        return None

    def get_auth_user(self, email, password):
        return self.get_auth_user_using_orm(email, password)

    @staticmethod
    def validate_auth_user_status(user):
        if not user.is_active:
            msg = _('User account is disabled.')
            raise Exception(msg)

    @staticmethod
    def validate_email_verification_status(user):
        if not hasattr(user, 'emailverification') or not user.emailverification.is_verified:
            msg = _('Account not Verified.')
            raise Exception(msg)

    def validate(self, attrs):
        email = attrs.get('email').lower()
        password = attrs.get('password')
        user = self.get_auth_user(email, password)

        if not user:
            msg = _('Unable to log in with provided credentials.')
            raise Exception(msg)

        # Did we get back an active user?
        self.validate_auth_user_status(user)

        # does the user have their email verified?
        self.validate_email_verification_status(user)

        attrs['user'] = user
        return attrs


class SetPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    def update(self, instance, validated_data):
        if validated_data['new_password'] != validated_data['confirm_password']:
            raise Exception("password fields don't match")
        print(instance.password)
        print(validated_data['new_password'])
        instance.set_password(validated_data['new_password'])
        print(instance.password)
        instance.save()
        return instance


class EmailVerificationSerializer(serializers.Serializer):
    token = serializers.UUIDField(required=True)

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ReadUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone_number',
            'full_name',
            'date_created',
            'date_updated',
        ]
        read_only_fields = fields


class Emailserialisers(serializers.Serializer):
    email = serializers.EmailField()
