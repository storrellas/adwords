from twilio.rest import Client as TwilioClient

from .baseclass import BaseClass
from ..helper import env


class Client(TwilioClient):
    """
    Customized Twilio Client Class.
    """

    def __init__(self):
        account_sid = env('TWILIO_ACCOUNT_SID')
        account_auth_token = env('TWILIO_AUTH_TOKEN')
        super().__init__(account_sid, account_auth_token)


class Twilio(BaseClass):

    #client: TwilioClient = Client()
    client = Client()

    def __init__(self):
        super().__init__()

    @classmethod
    def send_message(cls, to: str, message: str, _from: str = env('TWILIO_FROM_NUMBER')):
        return cls.client.messages.create(to, from_=_from, body=message)
