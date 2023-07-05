from rest_framework import serializers

from user_invest.models import UserInvestmentBalance, InvestmentRecord, InvestOptions, InvestmentType


class InvestmentSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    records = serializers.SlugRelatedField(slug_field="code", queryset=InvestmentRecord.objects.all())
    class Meta:
        model = UserInvestmentBalance
        fields = "__all__"


class RecordSerializers(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    options = serializers.SlugRelatedField(slug_field="code", queryset=InvestOptions.objects.all())
    class Meta:
        model = InvestmentRecord
        fields = "__all__"


class InvestOptionsSerializers(serializers.ModelSerializer):
    type = serializers.SlugRelatedField(slug_field="code", queryset=InvestmentType.objects.all())
    class Meta:
        model = InvestOptions
        fields = "__all__"


class InvestmentTypeSerializers(serializers.ModelSerializer):
    class Meta:
        model = InvestmentType
        fields = "__all__"
