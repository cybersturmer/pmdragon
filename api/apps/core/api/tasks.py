from __future__ import absolute_import, unicode_literals

from smtplib import SMTPException

from celery import shared_task
from django.contrib.auth import get_user_model
from django.conf import settings

from libs.email.compose import EmailComposer
from ..models import PersonRegistrationRequest, \
    PersonInvitationRequest, \
    IssueMessage, \
    Issue, \
    get_mentioned_user_ids, \
    Person, Workspace

User = get_user_model()


@shared_task
def send_registration_email(request_pk=None):
    request = PersonRegistrationRequest.objects.get(pk=request_pk)

    try:
        context = {
            'action_link': f'{settings.HOST_BY_DEFAULT}/verify/registration/{request.key}',
            'workspace': request.prefix_url,
            'expired_at': request.expired_at
        }

        EmailComposer().process(
            subject='PmDragon registration verification email',
            email=request.email,
            template='email/verification/registration.html',
            context=context
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
            if person not in request.workspace.participants.all():
                context = {
                    'action_link': f'{settings.HOST_BY_DEFAULT}/verify/collaboration/{request.key}',
                    'workspace': request.workspace.prefix_url,
                    'person': person,
                    'expired_at': request.expired_at
                }

                EmailComposer().process(
                    subject='PmDragon join workspace verification',
                    email=request.email,
                    template='email/verification/collaboration.html',
                    context=context
                )
        else:
            context = {
                'action_link': f'{settings.HOST_BY_DEFAULT}/verify/invitation/{request.key}',
                'workspace': request.workspace.prefix_url,
                'expired_at': request.expired_at
            }

            EmailComposer().process(
                subject='PmDragon invitation to workspace',
                email=request.email,
                template='email/verification/invitation.html',
                context=context
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
    mentioned_persons = get_mentioned_user_ids(message.description)

    try:
        for person_id in mentioned_persons:
            person = Person.objects.get(pk=int(person_id))
            context = {
                'issue_title': message.issue.title,
                'mentioned_by': message.created_by,
                'issue_message': message.description
            }

            EmailComposer().process(
                subject='PmDragon mentioned in issue message',
                email=person.email,
                template='email/messaging/mentioning.html',
                context=context
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
            context = {
                'issue_title': issue.title,
                'issue_description': issue.description
            }

            EmailComposer().process(
                subject='PmDragon mentioned in issue description',
                email=person.email,
                template='email/issue/mentioning.html',
                context=context
            )
    except SMTPException:
        pass

    return True
