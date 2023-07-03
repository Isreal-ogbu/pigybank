from dataclasses import dataclass

from django.contrib.auth import get_user_model

User = get_user_model()

"""Still under development"""
@dataclass
class paymentPayloadInfo:
    cardno: int
    cvv: int
    currency: int
    country: str
    expirymonth: int
    expiryyear: int
    amount: str
    email: str
    phonenumber: str
    firstname: str
    lastname: str
    IP: int
    user: User
