from smtplib import SMTPException

from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.permissions import AllowAny

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

        # @todo make wrapper for mailings
        try:
            send_mail(
                'You registration',
                f'Here is a message and a key {instance.key}',
                'welcome@pmdragon.org',
                [str(instance.email)],
                fail_silently=False
            )

        except SMTPException as smtp_error:
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
