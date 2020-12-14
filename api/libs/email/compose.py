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

    def _send(self):
        send_mail(
            subject=self.subject,
            html_message=self.html_message,
            message=self.message,
            from_email=self.from_email,
            recipient_list=[self.to_email],
            fail_silently=False,
        )

    def process(self, subject: str, email: str, template: str, context: dict):
        self.subject = subject
        self.html_message = render_to_string(template, context)
        self.to_email = email
        self._send()
