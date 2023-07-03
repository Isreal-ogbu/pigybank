from django.urls import path
from rest_framework import routers
from core import views

router = routers.DefaultRouter()

router.register(r"catagories", views.CatagoryViewSetApiView, basename='catagories')
router.register(r"transactions", views.TransactionViewSetApiView, basename='transactions')
router.register(r"currencies", views.CurrencySerializersApiView, basename='currency')

urlpatterns = [
    path('report', views.TransactionReportApiView.as_view(), name='report'),
] + router.urls
