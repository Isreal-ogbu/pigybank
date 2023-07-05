import uuid

from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Currency(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    code = models.CharField(max_length=3, unique=True)
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Catagory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='catagories')
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=32, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name='transactions')

    def __str__(self):
        return f"{self.amount} {self.date}"
