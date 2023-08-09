import json

from django.core.mail import send_mail
from django.core.signing import Signer

signer = Signer()


def sendMail():
    send_mail(
        "Testing phase of django",
        "Good WELCOME TO PYGGYBANK",
        "ogbuisreal@gmail.com",
        ["ogbuisreal@gmail.com"],
        fail_silently=False,
    )