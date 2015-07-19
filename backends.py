#-*- coding: utf-8 -*-

from __future__ import unicode_literals, print_function, absolute_import

import os

from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate
import smtplib


# for documentation only:
class BackendAPI(object):
    def __init__(self):
        """set everything up. fail here on missing configuration."""
        pass

    def send_message(self, to, from_email, subject, text):
        """send a single message to single to address"""
        pass

class MandrillBackend(object):

    def __init__(self):
        try:
            from mandrill import Mandrill
        except ImportError:
            raise Exception('Add mandrill to requirements.txt and pip install -r again to use mandrill')

        try:
            self.client = Mandrill(os.environ['MANDRILL_API_KEY'])
        except KeyError:
            raise Exception('Environment variable MANDRILL_API_KEY missing for mandrill backend')

    def send_message(self, to, from_email, subject, text):
        """Sends a message, returns True on success"""        

        message = {
               'to': [{'email': to}],
               'from_email': from_email,
               'subject': subject,
               'text': text,
        }

        result = self.client.messages.send(message=message)
        return result[0]['status'] == 'sent'
        
        
class SMTPBackend(object):
    """Send Mail via authenticated SMTP with configuration via environment or .netrc
    """
    def __init__(self):
        self.host = os.environ.get('FWDFORM_SMTPHOST')
        if not self.host:
            raise Exception("Prese set FWDFORM_SMTPHOST environment variable")

        self.username = os.environ.get('FWDFORM_SMTPUSERNAME')
        self.pwd = os.environ.get('FWDFORM_SMTPPASSWORD')
        

        if not self.username or not self.pwd:
            import netrc
            auth = netrc.netrc().authenticators(self.host)
            if not auth:
                raise Exception("Please set FWDFORM_SMTPUSERNAME and FWDFORM_SMTPPASSWORD environment variables or specify credentials in netrc")


            self.username, _, self.pwd = auth

    def send_message(self, to, from_email, subject, text):
        """Sends a message, returns True on success"""        

        msg = MIMEText(text, 'plain', 'utf8')
        msg['Subject'] = subject
        msg['To'] = to
        msg['From'] = from_email
        
        s = smtplib.SMTP_SSL()
        s.connect(host=self.host)
        s.login(self.username, self.pwd)
        try:
            s.sendmail(from_email, [to,], msg.as_string())
        except smtplib.SMTPException:
            return False
        finally:
            s.quit()   

        return True

backends = dict(mandrill=MandrillBackend,
                smtp=SMTPBackend)

