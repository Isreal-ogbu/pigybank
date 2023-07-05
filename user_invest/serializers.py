from rest_framework import serializers

from user_invest.models import UserInvestmentBalance, InvestmentRecord, InvestOptions, InvestmentType


class InvestmentSerializers(serializers.ModelSerializer):
    class Meta:
        models = UserInvestmentBalance
        fields = "__all__"


class RecordSerializers(serializers.ModelSerializer):
    class Meta:
        models = InvestmentRecord
        fields = "__all__"


class InvestOptionsSerializers(serializers.ModelSerializer):
    class Meta:
        models = InvestOptions
        fields = "__all__"


class InvestmentTypeSerializers(serializers.ModelSerializer):
    class Meta:
        models = InvestmentType
        fields = "__all__"
