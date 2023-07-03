from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('notification', views.EnquiryViewSet, basename='notification')

urlpatterns = [
              ] + router.urls
