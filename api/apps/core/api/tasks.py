from __future__ import absolute_import, unicode_literals

from smtplib import SMTPException

from celery import shared_task
from django.contrib.auth import get_user_model

from libs.email.compose import EmailComposer
from ..models import PersonRegistrationRequest, \
    PersonInvitationRequest, \
    IssueMessage, \
    Issue, \
    get_mentioned_user_ids, \
    Person

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

    user_with_email = User.objects.filter(email=request.email)

    try:

        if user_with_email.exists():
            person = user_with_email.get().person
            EmailComposer().verify_collaboration(
                key=request.key,
                prefix_url=request.workspace.prefix_url,
                expired_at=request.expired_at,
                person=person
            )
        else:
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


@shared_task
def send_mentioned_in_message_email(message_pk=None):
    message = IssueMessage.objects.get(pk=message_pk)

    mentioned_by_person = message.created_by
    mentioned_persons = get_mentioned_user_ids(message.description)

    try:
        for person_id in mentioned_persons:
            person = Person.objects.get(pk=int(person_id))
            EmailComposer().mentioning_in_issue_message(
                mentioned_by=mentioned_by_person,
                email=person.email
            )

    except SMTPException:
        pass

    return True


@shared_task
def send_mentioned_in_description_email(issue_pk=None):
    issue = Issue.objects.get(pk=issue_pk)
    mentioned_persons = get_mentioned_user_ids(issue.description)

    try:
        for person_id in mentioned_persons:
            person = Person.objects.get(pk=int(person_id))
            EmailComposer().mentioning_in_issue_description(
                email=person.email
            )
    except SMTPException:
        pass

    return True
