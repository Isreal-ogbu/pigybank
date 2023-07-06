from rest_framework import serializers

from user_invest.models import UserInvestmentBalance, InvestmentRecord, InvestOptions, InvestmentType


class InvestmentSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = UserInvestmentBalance
        fields = "__all__"


class RecordSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = InvestmentRecord
        fields = "__all__"


class InvestOptionsSerializers(serializers.ModelSerializer):
    class Meta:
        model = InvestOptions
        fields = "__all__"


class InvestmentTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = InvestmentType
        fields = "__all__"
