from datetime import datetime

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


class EmailComposer:
    def __init__(self):
        self.subject = ''
        self.message = ''
        self.html_message = ''
        self.from_email = settings.EMAIL_FROM_BY_DEFAULT
        self.to_email = ''

    def send(self):
        send_mail(
            subject=self.subject,
            html_message=self.html_message,
            message=self.message,
            from_email=self.from_email,
            recipient_list=[self.to_email],
            fail_silently=True,
        )

    def send_verification_email(self, key: str, prefix_url: str, expired_at: datetime, email: str):

        self.subject = 'PMDragon verification email'
        action_link = f'{settings.HOST_BY_DEFAULT}/verify?key={key}'
        context = {
            'action_link': action_link,
            'prefix_url': prefix_url,
            'expired_at': expired_at,
        }

        self.html_message = render_to_string('email/verification/verification.html', context)
        self.to_email = email
        self.send()




