from smtplib import SMTP as _SMTP

from autorecord.module.baseclass import BaseClass
from email.mime.text import MIMEText

from autorecord.module.helper import env


class SMTP(BaseClass, _SMTP):

    def __init__(self, host:str = env('SMTP_HOST'), port:str = env('SMTP_PORT')):
        super().__init__(host, port)

    @staticmethod
    def sendEmail(subject: str, message: str, _to: str):
        mail = SMTP()
        mail.send_mail(subject, message, _to)
        mail.quit()

    def send_mail(self, subject: str, message: str, _to: str or list, *args, **kwargs) -> dict:
        msg = MIMEText(message)
        msg['From'] = env('SMTP_FROM')
        msg['To'] = _to
        msg['Subject'] = subject

        return self.sendmail(msg['From'], msg['To'], msg.as_string(), *args, **kwargs)
