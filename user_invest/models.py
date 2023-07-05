import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class CommonFields(models.Model):
    id = models.UUIDField(default=uuid.uuid4(), primary_key=True, editable=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)


class InvestmentType(CommonFields):
    investment_type = models.CharField(max_length=100)

    def __int__(self):
        return f"{self.investment_type}"


class InvestOptions(models.Model):
    type = models.ForeignKey(InvestmentType, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    rio = models.CharField(max_length=6)
    duration = models.IntegerField(default=0)

    def __int__(self):
        return f"{self.name} - {self.duration}"


class InvestmentRecord(CommonFields):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    options = models.ForeignKey(InvestOptions, on_delete=models.PROTECT)

    def __int__(self):
        return f"{self.user.username}"


class UserInvestmentBalance(CommonFields):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.BigIntegerField(default=0)
    exp_rio = models.CharField(max_length=6)
    records = models.ForeignKey(InvestmentRecord, on_delete=models.PROTECT)

    def __int__(self):
        return f"{self.records.user.username}"
