from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

urlpatterns = [
    path('api/c/', include('core.urls')),
    path('api/n/', include('user_components.urls')),
    path('api/p/', include('user_payment.urls')),
    path('api/u/', include('user_management.urls')),
    path('api/i/', include('user_invest.urls')),
    path('api/admin/', admin.site.urls),
    path("__debug__/", include("debug_toolbar.urls")),
]
