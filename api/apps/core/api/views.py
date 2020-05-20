from smtplib import SMTPException

from rest_framework import generics
from rest_framework.permissions import AllowAny

from libs.email.compose import EmailComposer
from .serializers import *


class PersonRegistrationRequestCreateView(generics.CreateAPIView):
    """
    Create a user registration request by using email and URL prefix.
    After it generate an email with verification token and send it to chosen email.
    """
    queryset = PersonRegistrationRequest.valid.all()
    serializer_class = PersonRegistrationRequestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance: PersonRegistrationRequest = serializer.save()

        try:
            EmailComposer().send_verification_email(
                key=instance.key,
                prefix_url=instance.prefix_url,
                expired_at=instance.expired_at,
                email=instance.email
            )
        except SMTPException:
            instance.email_sent = False
            instance.save()

        else:
            instance.email_sent = True
            instance.save()


class PersonVerifyView(generics.CreateAPIView):
    """
    Create a Person linked to User after confirmation email.
    """
    queryset = Person.objects.all()
    serializer_class = PersonVerifySerializer
    permission_classes = [AllowAny]
