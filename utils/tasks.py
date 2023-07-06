from typing import Dict
from rave_python import Rave, RaveExceptions, Misc
from dotenv import load_dotenv
from decouple import config
from user_payment.data_class import paymentPayloadInfo

"""We need to break down this step into three endpoint"""
"""So this is still under development and not for the hackathon"""

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
