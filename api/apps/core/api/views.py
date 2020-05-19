from smtplib import SMTPException

from django.core.mail import send_mail
from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import *


class PersonRegistrationRequestCreateView(generics.CreateAPIView):
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
    queryset = Person.objects.all()
    serializer_class = PersonVerifySerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context.update({
            'key': self.kwargs['key'],
        })

        return context

