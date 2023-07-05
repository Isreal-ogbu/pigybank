from django.conf.urls import include
from django.urls import re_path as url
from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = "user_mgt"

router = DefaultRouter()

router.register('user', views.UsersSerializerViewSet, basename='user')
router.register('register', views.RegistrationViewSet, basename='register')
router.register('profile', views.UserViewSet, basename='profile')

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^login/$', views.LoginViewSet.as_view(), name="login"),
    url(r'^logout/$', views.LogoutViewSet.as_view(), name="logout"),
    url(r'^logoutall/$', views.LogoutAllView.as_view(), name="logoutall"),
    url(r'^set_password/<int:pk>/$', views.SetPasswordView.as_view(), name="set_password"),
    url(r'^verify-email/$', views.EmailVerificationViewSet.as_view(), name='verify_email'),
    url(r'^reverify-email/$', views.ReverificationViewSet.as_view(), name='reverify_email'),
]
