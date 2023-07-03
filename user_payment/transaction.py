from typing import Dict

import requests
from rave_python import Rave, RaveExceptions, Misc
from dotenv import load_dotenv
from decouple import config
from .models import UserPayment
import requests

load_dotenv()

rave = Rave(config('RAVE_PUBLIC_KEY'), config('RAVE_SECRET_KEY'))


def PaymentTransferTransaction(payload) -> Dict:
    """We will make this for collecting the tresaction payload"""
    try:
        res = rave.Card.charge(payload)
        print('res = ', res)
        if res["suggestedAuth"]:
            arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])
            if arg == "pin":
                pin = Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
                print('pin = ', pin)
            if arg == "address":
                address = Misc.updatePayload(res["suggestedAuth"], payload,
                                             address={"billingzip": "100218", "billingcity": "IKEJA",
                                                      "billingaddress": "470 Mundet PI", "billingstate": "LAGOS",
                                                      "billingcountry": "NG"})
                print('address = ', address)
            res = rave.Card.charge(payload)
            print('res1 =', res)
        if res["validationRequired"]:
            res = rave.Card.validate(res["flwRef"], "12345")
            print('res2 =', res)
        res = rave.Card.verify(res["txRef"])
        print('bool = ', res["transactionComplete"])
        print('res3 = ', res)
        return res
    except RaveExceptions.CardChargeError as e:
        print(e.err["errMsg"], e.err["flwRef"])
        return e.err
    except RaveExceptions.TransactionValidationError as e:
        print(e.err, e.err["flwRef"])
        return e.err
    except RaveExceptions.TransactionVerificationError as e:
        print(e.err["errMsg"], e.err["txRef"])
        return e.err
    except RaveExceptions.IncompletePaymentDetailsError as e:
        print(e.err["errMsg"])
        print(e.err["errMsg"])
    pass


def paymentDepositTransaction(payload) -> Dict:
    user = payload.get('app_user')
    appUser = UserPayment.objects.create(app_user=user)
    try:
        res = rave.Card.charge(payload)
        appUser.txRef = res['txRef']
        appUser.save()
        return res
    except RaveExceptions.CardChargeError as e:
        return e.err
    except RaveExceptions.IncompletePaymentDetailsError as e:
        return e.err


def ValidateSuggestedAuth(payload) -> Dict:
    """We want to validate by pin or by address from the payload"""
    try:
        appUser = UserPayment.objects.get(app_user=payload['user'], txf__exact=payload['txRef'])
    except Exception as e:
        return {'error': e}
    try:
        if payload["suggestedAuth"]:
            arg = Misc.getTypeOfArgsRequired(payload["suggestedAuth"])
            if arg == "pin":
                Misc.updatePayload(payload["suggestedAuth"], payload, pin=payload.get('pin', ''))
            if arg == "address":
                Misc.updatePayload(payload["suggestedAuth"], payload,
                                   address={"billingzip": "100218", "billingcity": "IKEJA",
                                            "billingaddress": "470 Mundet PI", "billingstate": "LAGOS",
                                            "billingcountry": "NG"})
            res = rave.Card.charge(payload)
            appUser.flwRef = res.get('flwRef', None)
            appUser.save()
            return res
    except RaveExceptions.CardChargeError as e:
        return e.err
    except RaveExceptions.IncompletePaymentDetailsError as e:
        return e.err


def CardTokenValidation(payload: Dict) -> Dict:
    response = GenerateToken(payload)
    try:
        if payload["validationRequired"]:
            rave.Card.validate(payload["flwRef"], response.get('otp', ""))
    except RaveExceptions.TransactionValidationError as e:
        return e.err


def GenerateToken(payload: Dict) -> Dict:
    data = {
        "length": 7,
        "customer": {
            "name": payload.get('firstname'),
            "email": payload.get('email'),
            "phone": payload.get('phone')
        },
        "sender": "COMPICODE",
        "send": True,
        "medium": [
            "email",
            "sms"
        ],
        "expiry": 5
    }
    headers = {"Authorization": 'Bearer ' + config('RAVE_SECRET_KEY'), 'Content-Type': 'application/json'}
    url = "https://api.flutterwave.com/v3/otps"
    res = requests.post(url, headers=headers, data=data)
    if res.status_code == 200:
        return res.json()
    return {}
