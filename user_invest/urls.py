from django.conf.urls import include
from django.urls import re_path as url
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()


router.register('invest', views.InvestmentOptionsViewSet, basename='register')
router.register('type', views.InvestTypeViewSet, basename='investment_type')
router.register('record', views.InvestmentRecordViewSet, basename='investment_record')

urlpatterns = [
    url(r'^balance/$', views.BalanceViewset.as_view(), name="balance"),
] + router.urls
