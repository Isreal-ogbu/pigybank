from django.contrib.auth.models import User
from rest_framework import serializers

from core.models import Currency, Catagory, Transaction
from utils.report import ReportParams


class ReadUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', "last_name")


class CurrencySerializers(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['id', 'code', "name"]


class CatagoryViewSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Catagory
        fields = ('id', 'name', 'user')


class WriteTransactionSerializers(serializers.ModelSerializer):
    """To authomatically serialize authenticated user without send it with the payload"""
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    currency = serializers.SlugRelatedField(slug_field="code", queryset=Currency.objects.all())

    def __int__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = self.context['request'].user
        self.fields["catagory"].queryset = user.catagories.all()

    class Meta:
        model = Transaction
        fields = (
            "amount",
            "currency",
            "date",
            "description",
            "catagory",
            'user',
        )


class ReadTransactionSerializers(serializers.ModelSerializer):
    user = ReadUserSerializers()
    currency = CurrencySerializers()
    catagory = CatagoryViewSerializer()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "amount",
            "currency",
            "date",
            "description",
            "catagory",
            "user",
        )


class ReportEntrySerializers(serializers.Serializer):
    catagory = CatagoryViewSerializer()
    total = serializers.DecimalField(max_digits=15, decimal_places=2)
    count = serializers.IntegerField()
    avg = serializers.DecimalField(max_digits=15, decimal_places=2)


class ReportParamSerializers(serializers.Serializer):
    start_date = serializers.DateTimeField()
    end_date = serializers.DateTimeField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def create(self, validated_data):
        return ReportParams(**validated_data)
