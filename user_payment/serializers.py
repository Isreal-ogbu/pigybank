from rest_framework import serializers
from user_payment.data_class import paymentPayloadInfo
from user_payment.models import UserPayment


class PaymentSerializers(serializers.Serializer):
    cardno = serializers.CharField(max_length=16, min_length=16)
    cvv = serializers.CharField(max_length=3, min_length=3)
    currency = serializers.CharField(max_length=100)
    country = serializers.CharField(max_length=50)
    expirymonth = serializers.CharField(max_length=50)
    expiryyear = serializers.CharField(max_length=50)
    amount = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    phonenumber = serializers.CharField(max_length=11, min_length=11)
    firstname = serializers.CharField(max_length=50)
    lastname = serializers.CharField(max_length=50)
    IP = serializers.IPAddressField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return validated_data


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=7, min_length=6)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


class SuggestedAuthSeializer(serializers.Serializer):
    pin = serializers.CharField(max_length=7, min_length=6, allow_blank=True, allow_null=True)
    billingzip = serializers.CharField(max_length=7, min_length=6, allow_blank=True, allow_null=True)
    billingcity = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    billingaddress = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    billingstate = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    billingcountry = serializers.CharField(max_length=200, allow_null=True, allow_blank=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    def validate(self, attrs):
        if not attrs['pin'] or not attrs['billingzip'] and not attrs['billingcity'] and not attrs['billingaddress'] and not attrs['billingstate'] and not attrs['billingcountry']:
            raise serializers.ValidationError('User pin or address details required')
        return attrs
