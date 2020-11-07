from __future__ import absolute_import, unicode_literals

from smtplib import SMTPException

from celery import shared_task
from django.contrib.auth import get_user_model

from libs.email.compose import EmailComposer
from ..models import PersonRegistrationRequest, PersonInvitationRequest

User = get_user_model()


@shared_task
def send_registration_email(request_pk=None):
    request = PersonRegistrationRequest.objects.get(pk=request_pk)

    try:
        EmailComposer().verify_registration(
            key=request.key,
            prefix_url=request.prefix_url,
            expired_at=request.expired_at,
            email=request.email
        )
    except SMTPException:
        request.is_email_sent = False
        request.save()

    else:
        request.is_email_sent = True
        request.save()

    return True


@shared_task
def send_invitation_email(request_pk=None):
    request = PersonInvitationRequest.valid.get(pk=request_pk)

    try:
        EmailComposer().verify_invitation(
            key=request.key,
            prefix_url=request.workspace.prefix_url,
            expired_at=request.expired_at,
            email=request.email
        )
    except SMTPException:
        request.is_email_sent = False
        request.save()

    else:
        request.is_email_sent = True
        request.save()

    return True
