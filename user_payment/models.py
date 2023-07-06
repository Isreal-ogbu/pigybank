import uuid

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()
"""Still under development"""

class UserPayment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    app_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userpayment')
    error = models.BooleanField(default=False)
    validationRequired = models.BooleanField(default=False)
    txRef = models.CharField(max_length=16, blank=True, null=True)
    flwRef = models.CharField(max_length=42, blank=True, null=True)
    suggestedAuth = models.CharField(max_length=6, blank=True, null=True)
    authUrl = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=7, blank=True, null=True)
    message = models.CharField(max_length=30, blank=True, null=True)
    transactionComplete = models.BooleanField(default=False)
    amount = models.BigIntegerField(default=0)
    chargedAmount = models.BigIntegerField(default=0)
    token = models.CharField(max_length=7)
    cardToken = models.CharField(max_length=100, blank=True, null=True)
    vbmessage = models.CharField(max_length=50, blank=True, null=True)
    chargeMessage = models.CharField(max_length=200, blank=True, null=True)
    chargeCode = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=5, blank=True, null=True)
    meta = models.JSONField(default=list, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.app_user} - checkout_id: {self.txRef}"
