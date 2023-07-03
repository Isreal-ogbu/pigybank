from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from utils.util import ResponseModelViewSet
from utils.permissions import SuperAdminPermission, AdminUserPermission, AuthenticatedUserPermission

from core.models import Currency
from utils.report import transaction_report
from core.serializers import CurrencySerializers, CatagoryViewSerializer, \
    ReadTransactionSerializers, WriteTransactionSerializers, ReportEntrySerializers, ReportParamSerializers


class CurrencySerializersApiView(ResponseModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializers
    permission_classes = (SuperAdminPermission,)

    def get_permissions(self):
        print(self.request.user.is_staff, self.action)
        if self.action in ['list', 'retrieve']:
            return [SuperAdminPermission() and AdminUserPermission() and AuthenticatedUserPermission()]
        elif self.action in ['create', 'update']:
            return [AdminUserPermission()]
        return super().get_permissions()


class CatagoryViewSetApiView(ResponseModelViewSet):
    serializer_class = CatagoryViewSerializer
    permission_classes = (SuperAdminPermission,)

    def get_queryset(self):
        return self.request.user.catagories.select_related('user').filter(user=self.request.user)

    def get_permissions(self):
        print(self.request.user.is_staff, self.action)
        if self.action in ['list', 'retrieve']:
            return [SuperAdminPermission() and AdminUserPermission() and AuthenticatedUserPermission()]
        elif self.action in ['create', 'update']:
            return [AdminUserPermission()]
        return super().get_permissions()


class TransactionViewSetApiView(ResponseModelViewSet):
    filter_backends = [OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['date']
    filterset_fields = ['currency__code', "catagory__name", "amount"]
    permission_classes = (SuperAdminPermission,)

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return ReadTransactionSerializers
        return WriteTransactionSerializers

    def get_queryset(self):
        return self.request.user.transactions.select_related("currency", "catagory", "user").filter(
            user=self.request.user).order_by('-date')

    def get_permissions(self):
        print(self.request.user.is_staff, self.action)
        if self.action in ['list', 'retrieve']:
            return [SuperAdminPermission() and AdminUserPermission() and AuthenticatedUserPermission()]
        elif self.action in ['create', 'update']:
            return [AdminUserPermission()]
        return super().get_permissions()


class TransactionReportApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        personal_report = ReportParamSerializers(data=request.GET, context={'request': request})
        personal_report.is_valid(raise_exception=True)
        param = personal_report.save()
        data = transaction_report(param)
        serializers = ReportEntrySerializers(instance=data, many=True)
        return Response(
            {
                "status": 'Success',
                "data": serializers.data,
                "message": 'Success'
            }, status=status.HTTP_200_OK
        )

