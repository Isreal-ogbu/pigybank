from django.conf.urls import include
from django.urls import re_path as url, path
from . import views
from rest_framework.routers import DefaultRouter, SimpleRouter

app_name = "user_mgt"

router = DefaultRouter()

router.register('user', views.UsersSerializerViewSet, basename='user')
router.register('register', views.RegistrationViewSet, basename='register')
router.register('profile', views.UserViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', views.LoginViewSet.as_view(), name="login"),
    path('logout/', views.LogoutViewSet.as_view(), name="logout"),
    path('logoutall/', views.LogoutAllView.as_view(), name="logoutall"),
    path('set-password/<uuid:user_id>/', views.SetPasswordView.as_view(), name="set_password"),
    path('verify-email/', views.EmailVerificationViewSet.as_view(), name='verify_email'),
    path('reverify-email/', views.ReverificationViewSet.as_view(), name='reverify_email'),
]
