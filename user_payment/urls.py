from django.conf.urls import include
from django.urls import re_path as url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

"""Still Under development"""

router.register('status', views.TokenViewSet, basename='status')

urlpatterns = [
    url(r'^payment_successful/$', views.PaymentSuccessViewset.as_view(), name="payment_success"),
    url(r'^payment_cancelled/$', views.PaymentCancelledViewset.as_view(), name="payment_cancelled"),
    url(r'^hook/$', views.PaymentWebhookViewSet.as_view(), name="Payment_webhooks"),
]
