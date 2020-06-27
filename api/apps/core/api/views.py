from smtplib import SMTPException

from django.utils.translation import ugettext_lazy as _
from rest_framework import viewsets, generics, mixins, status
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from libs.email.compose import EmailComposer
from .schemas import IssueListUpdateSchema
from .serializers import *


class TokenObtainPairExtendedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refreshes JSON web
    token pair to prove the authentication of those credentials.
    Ext: Also returns user data such as
    [email, first name, last name, expired_at for tokens]
     to reduce logic from frontend web application.
    """
    serializer_class = TokenObtainPairExtendedSerializer


class PersonRegistrationRequestCreateView(generics.CreateAPIView,
                                          viewsets.ViewSetMixin):
    """
    Create a user registration request by using email and URL prefix.
    After it generates an email with verification token and sends it to chosen email.
    """
    queryset = PersonRegistrationRequest.valid.all()
    serializer_class = PersonRegistrationRequestSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        instance: PersonRegistrationRequest = serializer.save()

        try:
            # @todo Better to do it asynchronously (Celery, RabbitMQ)?
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


class PersonVerifyView(generics.CreateAPIView,
                       viewsets.ViewSetMixin):
    """
    Create a Person object linked to User after confirmation email.
    """
    queryset = Person.objects.all()
    serializer_class = PersonVerifySerializer
    permission_classes = [AllowAny]


class WorkspaceReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get all workspaces current Person participate in
    We need it on frontend to understand list of workspaces to switch between
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkspaceSerializer
    queryset = Workspace.objects.all()

    def get_queryset(self):
        queryset = super(WorkspaceReadOnlyViewSet, self).get_queryset()
        return queryset.filter(
            participants__in=[self.request.user.person]
        ).all()


class WorkspacesReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    WORKSPACE_PERMISSIONS_NOTIFICATION = _('You do not have permissions for this workspace')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Getting all instances, that belong to this workspace. """
        queryset = super(WorkspacesReadOnlyModelViewSet, self).get_queryset()
        queryset = queryset. \
            filter(workspace__participants__in=[self.request.user.person])

        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'person': self.request.user.person
        })

        return context


class WorkspacesModelViewSet(WorkspacesReadOnlyModelViewSet,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin):
    pass


class ProjectViewSet(WorkspacesModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IssueTypeCategoryViewSet(WorkspacesModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = IssueTypeCategory.objects.all()
    serializer_class = IssueTypeSerializer


class IssueStateCategoryViewSet(WorkspacesModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = IssueStateCategory.objects.all()
    serializer_class = IssueStateSerializer


class IssueViewSet(WorkspacesModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'person': self.request.user.person
        })

        return context


class ProjectBacklogViewSet(WorkspacesReadOnlyModelViewSet,
                            mixins.UpdateModelMixin):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = ProjectBacklog.objects.all()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return BacklogReadOnlySerializer
        else:
            return BacklogWritableSerializer


class SprintDurationViewSet(WorkspacesModelViewSet):
    """
    Workspace based set.
    See class, that was extended.
    """
    queryset = SprintDuration.objects.all()
    serializer_class = SprintDurationSerializer


class SprintViewSet(WorkspacesModelViewSet):
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


class IssueListUpdateApiView(UpdateAPIView):
    """
    Bulk update issues ordering, doesn't matter is it a Backlog
    or Sprint or Agile Board.
    """
    schema = IssueListUpdateSchema()
    serializer_class = IssueChildOrderingSerializer

    def get_serializer(self, *args, **kwargs):
        return super(IssueListUpdateApiView, self).get_serializer(*args, **kwargs)

    def get_queryset(self, ids=None):
        queryset = Issue.objects.filter(workspace__participants__in=[self.request.user.person])

        if ids is None:
            return queryset

        return queryset.filter(id__in=ids)

    def update(self, request, *args, **kwargs):
        ids = validate_ids(data=request.data)
        instances = self.get_queryset(ids=ids)
        serializer = self.get_serializer(
            instances, data=request.data, partial=False, many=True
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


def validate_ids(data, field='id', unique=True):
    if isinstance(data, list):
        id_list = [int(x[field]) for x in data]

        if unique and len(id_list) != len(set(id_list)):
            raise ValidationError(_('Multiple updates of single field found'))

        return id_list
    return [data]


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
