import uuid
from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin, AbstractUser
from django.db import models


class UserProfileManager(BaseUserManager):
    """User management model for all user"""
    def create_user(self, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Users Must Have an email address')
        user = self.model(
            email=self.normalize_email(email.lower()),
            username=self.normalize_email(email.lower()),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, password, email=None, **extra_fields):
        if password is None:
            raise TypeError('Superusers must have a password.')
        user = self.create_user(email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        return user


class User(AbstractUser, PermissionsMixin):
    """User_id is set to uuid4 field as required"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField("First Name", max_length=100, blank=True)
    last_name = models.CharField("Last Name", max_length=100, blank=True)
    email = models.EmailField('email address', unique=True, db_index=True)
    username = models.CharField(max_length=100, unique=False, null=True, default=None)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def full_name(self):
        return self.first_name + " - " + self.last_name


class EmailVerification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emailverification')
    token = models.UUIDField(default=uuid.uuid4, editable=False)
    is_verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.token)
