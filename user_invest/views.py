from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from utils.util import ResponseAPIView, ResponseModelViewSet
from .serializers import InvestmentSerializers, RecordSerializers, InvestOptionsSerializers, InvestmentTypeSerializers
from .models import InvestmentType, InvestmentRecord, UserInvestmentBalance, InvestOptions
from utils.permissions import SuperAdminPermission, AdminUserPermission, AuthenticatedUserPermission


class BalanceViewset(ResponseAPIView):
    serializer_class = InvestmentSerializers
    permission_classes = (AuthenticatedUserPermission,)

    def get_queryset(self):
        return UserInvestmentBalance.objects.select_related('user', 'records').filter(user=self.request.user)

    def post(self, request, **kwargs):
        serializer = InvestmentSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        self.response_format['data'] = serializer.data
        return Response(self.response_format, self.status_code)

    def get(self, request, pk, **kwargs):
        return super().get_object()


class InvestmentRecordViewSet(ResponseModelViewSet):
    serializer_class = RecordSerializers
    permission_classes = (AuthenticatedUserPermission,)

    def get_queryset(self):
        return InvestmentRecord.objects.select_related('user', 'options').filter(user=self.request.user)


class InvestTypeViewSet(ResponseModelViewSet):
    queryset = InvestmentType.objects.all()
    serializer_class = InvestmentTypeSerializers
    permission_classes = (SuperAdminPermission,)

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [SuperAdminPermission() and AdminUserPermission() and AuthenticatedUserPermission()]
        return super().get_permissions()


class InvestmentOptionsViewSet(ResponseModelViewSet):
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['-date_created']
    filterset_fields = ['type', 'name']
    permission_classes = (SuperAdminPermission,)
    queryset = InvestOptions.objects.all()
    serializer_class = InvestOptionsSerializers

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [SuperAdminPermission() and AdminUserPermission() and AuthenticatedUserPermission()]
        return super().get_permissions()
