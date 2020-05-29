from smtplib import SMTPException

from django.utils.translation import ugettext_lazy as _
from rest_framework import generics, viewsets, mixins, status
from rest_framework.exceptions import NotAuthenticated
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from libs.email.compose import EmailComposer
from .serializers import *


class TokenObtainPairExtendedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    Ext: Also returns user data such as
    [email, first name, last name, expired_at for tokens]
     to reduce logic from frontend web.
    """
    serializer_class = TokenObtainPairExtendedSerializer


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
    One of the 2 way to create Person in system
    """
    queryset = Person.objects.all()
    serializer_class = PersonVerifySerializer
    permission_classes = [AllowAny]


class WorkspaceReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Workspace is the way to isolate environments of different users
    between each other.
    We extend this class to get view for auth user with checking of
    participating in Workspace.
    This Class is Read Only.
    """
    WORKSPACE_PERMISSIONS_NOTIFICATION = _('You do not have permissions for this workspace')
    permission_classes = (IsAuthenticated, )

    def is_participant(self, workspace: Workspace) -> bool:
        return self.request.user.person in workspace.participants.all()

    def get_workspace(self) -> Workspace:
        workspace_url = self.kwargs.get('workspace')

        if workspace_url is None:
            raise NotAuthenticated(detail=self.WORKSPACE_PERMISSIONS_NOTIFICATION)

        try:
            workspace = Workspace.objects.get(prefix_url__exact=workspace_url)
            if not self.is_participant(workspace):
                raise Workspace.DoesNotExist

        except Workspace.DoesNotExist:
            raise NotAuthenticated(detail=self.WORKSPACE_PERMISSIONS_NOTIFICATION)

        self.kwargs.update({'workspace': workspace})

        return workspace

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'workspace': self.kwargs.get('workspace')})

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        workspace = self.get_workspace()
        queryset = queryset.filter(workspace_id=workspace.pk)

        return queryset


class WorkspaceModelViewSet(WorkspaceReadOnlyModelViewSet,
                            mixins.CreateModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin):
    """
    Workspace is the way to isolate environments of different users
    between each other.
    We extend this class to get view for auth user with checking of
    participating in Workspace.
    This class is editable. So currently to be be part of workspace
     is enough to do whatever you want
    """
    def perform_create(self, serializer):
        workspace: Workspace = self.get_workspace()
        serializer.save(workspace=workspace)


class ProjectViewSet(WorkspaceModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IssueTypeCategoryViewSet(WorkspaceModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = IssueTypeCategory.objects.all()
    serializer_class = IssueTypeCategorySerializer


class IssueStateCategoryViewSet(WorkspaceModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = IssueStateCategory.objects.all()
    serializer_class = IssueStateCategorySerializer


class IssueViewSet(WorkspaceModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class ProjectBacklogViewSet(WorkspaceReadOnlyModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = ProjectBacklog.objects.all()
    serializer_class = ProjectBacklogSerializer


class SprintDurationViewSet(WorkspaceModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = SprintDuration.objects.all()
    serializer_class = SprintDurationSerializer


class SprintViewSet(WorkspaceModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer


class PersonSetPasswordView(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSetPasswordSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Set password for user
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'detail': _('New password has been saved.')},
                        status=status.HTTP_200_OK)


"""
@todo
Class LogoutView
Look at: 
https://github.com/Tivix/django-rest-auth/blob/624ad01afbc86fa15b4e652406f3bdcd01f36e00/rest_auth/views.py#L109
"""

"""
@todo
Class PasswordReset
Look at:
https://github.com/Tivix/django-rest-auth/blob/624ad01afbc86fa15b4e652406f3bdcd01f36e00/rest_auth/views.py#L195
"""

"""
@todo
Class PasswordResetConfirm
Look at:
https://github.com/Tivix/django-rest-auth/blob/624ad01afbc86fa15b4e652406f3bdcd01f36e00/rest_auth/views.py#L195
"""