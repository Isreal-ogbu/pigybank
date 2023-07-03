from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_payment.serializers import PaymentSerializers, TokenSerializer
from user_payment.transaction import CardTokenValidation
from utils.tasks import PaymentTransferTransaction
from utils.util import ResponseAPIView, ResponseModelViewSet

User = get_user_model()


class UserRecordsViewSet(ResponseModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializers
    http_method_names = ['post']

    def post(self, request, **kwargs):
        serializer = PaymentSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        params = serializer.save()
        data = PaymentTransferTransaction(params)
        return Response({
            "status": 'Success',
            "data": data,
            "message": 'Transaction Successful'
        }, status=status.HTTP_200_OK)


class TokenViewSet(ResponseAPIView):
    serializer_class = TokenSerializer

    def post(self, request, **kwargs):
        serializer = TokenSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        data = serializer.save()
        data = CardTokenValidation(data)
        self.response_format['data'] = data
        return Response(self.response_format, status=self.status_code)


class PaymentValidationViewSet(ResponseModelViewSet):
    pass


class PaymentSuccessViewset(ResponseAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PaymentSerializers
    http_method_names = ['post']

    def post(self, request, **kwargs):
        serializer = PaymentSerializers(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        params = serializer.save()
        data = PaymentTransferTransaction(params)
        return Response({
            "status": 'Success',
            "data": data,
            "message": 'Transaction Successful'
        }, status=status.HTTP_200_OK)

    def get_queryset(self):
        return User.objects.get(id=self.request.user.id)


class PaymentCancelledViewset(ResponseAPIView):
    pass


class PaymentWebhookViewSet(ResponseAPIView):
    pass
