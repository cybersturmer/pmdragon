from smtplib import SMTPException

from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, viewsets
from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import AllowAny, IsAuthenticated

from libs.email.compose import EmailComposer
from .serializers import *


class PersonRegistrationRequestCreateView(generics.CreateAPIView,
                                          viewsets.ViewSetMixin):
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


class PersonVerifyView(generics.CreateAPIView, viewsets.ViewSetMixin):
    """
    Create a Person linked to User after confirmation email.
    """
    queryset = Person.objects.all()
    serializer_class = PersonVerifySerializer
    permission_classes = [AllowAny]


class WorkspaceModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    PERMISSIONS_NOTIFICATION = _('You do not have permissions for this workspace')

    def get_workspace(self) -> Workspace:
        workspace_url = self.kwargs.get('workspace')

        if workspace_url is None:
            raise NotAuthenticated(detail=self.PERMISSIONS_NOTIFICATION)

        try:
            workspace = Workspace.objects.get(prefix_url__exact=workspace_url)
            if self.request.user.person not in workspace.participants.all():
                raise Workspace.DoesNotExist

        except Workspace.DoesNotExist:
            raise NotAuthenticated(detail=self.PERMISSIONS_NOTIFICATION)

        self.kwargs.update({'workspace': workspace})

        return workspace

    def get_serializer_context(self):
        context = super(WorkspaceModelViewSet, self).get_serializer_context()
        context.update({'workspace': self.kwargs.get('workspace')})

        return context

    def get_queryset(self):
        queryset = super(WorkspaceModelViewSet, self).get_queryset()

        workspace = self.get_workspace()
        queryset = queryset.filter(workspace_id=workspace.pk)

        return queryset

    def perform_create(self, serializer):
        workspace: Workspace = self.get_workspace()
        serializer.save(workspace=workspace)


class ProjectViewSet(WorkspaceModelViewSet):
    """
    Create a Project
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IssueTypeCategoryViewSet(WorkspaceModelViewSet):
    queryset = IssueTypeCategory.objects.all()
    serializer_class = IssueTypeCategorySerializer


class IssueStateCategoryViewSet(WorkspaceModelViewSet):
    queryset = IssueStateCategory.objects.all()
    serializer_class = IssueStateCategorySerializer


class IssueViewSet(WorkspaceModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class ProjectBacklogViewSet(WorkspaceModelViewSet):
    queryset = ProjectBacklog.objects.all()
    serializer_class = ProjectBacklogSerializer
