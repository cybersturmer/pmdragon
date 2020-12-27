from django.contrib.auth.admin import sensitive_post_parameters_m
from django.utils.translation import ugettext_lazy as _
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, generics, mixins, status, views
from rest_framework.generics import GenericAPIView, UpdateAPIView
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

from .schemas import IssueListUpdateSchema
from .serializers import *
from .tasks import send_registration_email, send_invitation_email
from .permissions import IsParticipateInWorkspace, IsCreatorOrReadOnly


class TokenObtainPairExtendedView(TokenObtainPairView):
    """
    Takes a set of user credentials and returns an access and refreshes JSON web
    token pair to prove the authentication of those credentials.
    Ext: Also returns user data such as
    [email, first name, last name, expired_at for tokens]
     to reduce logic from frontend web application.
    """
    serializer_class = TokenObtainPairExtendedSerializer


class PersonRegistrationRequestView(viewsets.GenericViewSet,
                                    mixins.RetrieveModelMixin,
                                    mixins.CreateModelMixin):
    """
    Create a user registration request by using email and URL prefix.
    It also can be used to get registration request by given key
    """
    queryset = PersonRegistrationRequest.valid.all()
    serializer_class = PersonRegistrationRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    lookup_field = 'key'

    def perform_create(self, serializer):
        instance: PersonRegistrationRequest = serializer.save()

        # Send verification email to user on request
        send_registration_email.delay(instance.pk)
        instance.save()

        return True


class PersonInvitationRequestRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """
    Can to be used for check does invitation requests exists by key.
    It also can be used to update state of requests, mark it as accepted.
    """
    queryset = PersonInvitationRequest.valid.all()
    serializer_class = PersonInvitationRequestRetrieveUpdateSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    lookup_field = 'key'
    http_method_names = (
        'head',
        'options',
        'get',
        'put'
    )


class PersonInvitationRequestListView(generics.ListAPIView):
    queryset = PersonInvitationRequest.valid.all()
    serializer_class = PersonInvitationRequestSerializer
    permission_classes = (
        IsAuthenticated,
        IsParticipateInWorkspace
    )


class PersonInvitationRequestListCreateView(generics.ListCreateAPIView):
    """
    Can be useful for bulk create requests by giving
    1) Email
    2) Workspace prefix
    """
    queryset = PersonInvitationRequest.valid.all()
    serializer_class = PersonInvitationRequestList
    http_method_names = (
        'post',
        'head',
        'options'
    )

    def create(self, request, *args, **kwargs):
        requested_person = request.user.person

        try:
            invitations = request.data['invites']
        except KeyError:
            raise ValidationError(_('Invalid data. Expected a invites key in dictionary.'))

        if type(invitations) is not list:
            raise ValidationError(_('Invalid data. Expected a list'))

        invitations_response = []

        for invitation in invitations:
            _workspace_with_pk = Workspace.objects \
                .filter(pk=invitation['workspace'],
                        participants__in=[requested_person])

            if not _workspace_with_pk.exists():
                raise ValidationError(_('Workspace with given prefix and available for you does not exists'))

            _workspace = _workspace_with_pk.get()

            _email = invitation['email']

            """
            If person already in given workspace - we don't need to send him invitation """
            _user_with_email = User.objects.filter(email=_email)
            if _user_with_email.exists():
                _user = _user_with_email.get()
                _person = _user.person
                if _person in _workspace.participants.all():
                    break

            _invitation_request = PersonInvitationRequest(
                email=_email,
                workspace=_workspace
            )

            _invitation_request.save()

            send_invitation_email.delay(_invitation_request.pk)
            serializer = PersonInvitationRequestSerializer(_invitation_request)
            invitations_response.append(serializer.data)

        return Response(data=invitations_response,
                        status=status.HTTP_201_CREATED)


class PersonInvitationRequestViewSet(viewsets.GenericViewSet,
                                     mixins.RetrieveModelMixin,
                                     mixins.CreateModelMixin):
    queryset = PersonInvitationRequest.valid.all()
    serializer_class = PersonInvitationRequestSerializer
    lookup_field = 'key'


class PersonInvitationRequestAcceptView(viewsets.GenericViewSet,
                                        mixins.UpdateModelMixin):
    """
    Accept collaboration request for already registered persons.
    """
    queryset = PersonInvitationRequest.valid.all()
    serializer_class = PersonInvitationRequestSerializer
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle]
    lookup_field = 'key'


class PersonRegistrationRequestVerifyView(generics.CreateAPIView,
                                          viewsets.ViewSetMixin):
    """
    Create a Person object linked to User after confirmation email.
    """
    queryset = Person.objects.all()
    serializer_class = PersonRegistrationOrInvitationRequestSerializer
    permission_classes = [AllowAny]


class CollaboratorsViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Getting all persons in available workspaces
    """
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def get_queryset(self):
        workspaces = Workspace.objects \
            .filter(participants__in=[self.request.user.person]) \
            .all()

        collaborators = []
        for workspace in workspaces:
            for participant in workspace.participants.all():
                collaborators.append(participant.id)

        collaborators_set = set(collaborators)

        queryset: Person.objects = super(CollaboratorsViewSet, self).get_queryset()

        return queryset.filter(id__in=collaborators_set).all()


class WorkspaceViewSet(viewsets.ModelViewSet):
    """
    Writable endpoint for workspaces
    Of course we need to add information about current person
    to created_by and participant
    """
    permission_classes = (IsAuthenticated, IsCreatorOrReadOnly)
    serializer_class = WorkspaceWritableSerializer
    queryset = Workspace.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return WorkspaceDetailedSerializer
        else:
            return WorkspaceWritableSerializer

    def get_serializer_context(self):
        """
        Put to serializer context information about current person
        """
        context = super().get_serializer_context()
        context.update({
            'person': self.request.user.person
        })

        return context

    def create(self, request, *args, **kwargs):
        workspace_data = request.data

        short_serializer = WorkspaceWritableSerializer(
            data=workspace_data,
            context={'person': self.request.user.person}
        )

        if not short_serializer.is_valid():
            return Response(
                data=short_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        short_serializer.save()
        detailed_serializer = WorkspaceDetailedSerializer(instance=short_serializer.instance)

        return Response(
            data=detailed_serializer.data,
            status=status.HTTP_201_CREATED
        )


class WorkspaceReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Get all workspaces current Person participate in
    We need it on frontend to understand list of workspaces to switch between
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = WorkspaceDetailedSerializer
    queryset = Workspace.objects.all()

    def get_queryset(self):
        queryset = super(WorkspaceReadOnlyViewSet, self).get_queryset()
        return queryset.filter(
            participants__in=[self.request.user.person]
        ).all()


class WorkspacesReadOnlyModelViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Extendable class to have read only ViewSet of any instance, that have
    workspace isolation.
    """
    WORKSPACE_PERMISSIONS_NOTIFICATION = _('You do not have permissions for this workspace')
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Getting all instances, that belong to this workspace.
        """
        queryset = super(WorkspacesReadOnlyModelViewSet, self).get_queryset()
        queryset = queryset. \
            filter(workspace__participants__in=[self.request.user.person])

        return queryset

    def get_serializer_context(self):
        """
        Put to serializer context information about current person
        """
        context = super().get_serializer_context()
        context.update({
            'person': self.request.user.person
        })

        return context


class WorkspacesModelViewSet(WorkspacesReadOnlyModelViewSet,
                             mixins.CreateModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin):
    """
    Extendable class to have writable ViewSet,
    that have isolation by workspaces.
    """
    pass


class ProjectViewSet(WorkspacesModelViewSet):
    """
    View for getting, editing, deleting instance.
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class IssueTypeCategoryViewSet(WorkspacesModelViewSet):
    """
    View for getting, editing, deleting instance.
    """
    queryset = IssueTypeCategory.objects.all()
    serializer_class = IssueTypeSerializer


class IssueStateCategoryViewSet(WorkspacesModelViewSet):
    """
    View for getting, editing, deleting instance.
    """
    queryset = IssueStateCategory.objects.all()
    serializer_class = IssueStateSerializer


class IssueEstimationCategoryViewSet(WorkspacesModelViewSet):
    queryset = IssueEstimationCategory.objects.all()
    serializer_class = IssueEstimationSerializer
    permission_classes = (
        IsAuthenticated,
        IsParticipateInWorkspace
    )


class IssueViewSet(WorkspacesModelViewSet):
    """
    View for getting, editing, deleting instance.
    """
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class IssueMessagesViewSet(WorkspacesModelViewSet):
    queryset = IssueMessage.objects.all()
    serializer_class = IssueMessageSerializer
    permission_classes = (
        IsAuthenticated,
        IsParticipateInWorkspace,
        IsCreatorOrReadOnly
    )
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['issue']


class ProjectBacklogViewSet(WorkspacesReadOnlyModelViewSet,
                            mixins.UpdateModelMixin):
    """
    View for getting, editing, instance.
    """
    queryset = ProjectBacklog.objects.all()
    serializer_class = BacklogWritableSerializer


class SprintDurationViewSet(WorkspacesModelViewSet):
    """
    View for getting, editing, deleting instance.
    """
    queryset = SprintDuration.objects.all()
    serializer_class = SprintDurationSerializer


class SprintViewSet(WorkspacesModelViewSet):
    """
    View for getting, editing, deleting instance.
    """
    queryset = Sprint.objects.all()
    serializer_class = SprintWritableSerializer


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


class PersonAvatarUpload(views.APIView):
    """
    Person avatar picture APIView
    """
    parser_classes = [MultiPartParser]

    def put(self, request):
        file_obj = request.data['image']

        person: Person = self.request.user.person
        person.avatar.save(file_obj.name, file_obj)
        person.save()

        avatar_url = request.build_absolute_uri(person.avatar.url)

        response_data = {
            'avatar': avatar_url
        }

        return Response(
            data=response_data,
            status=status.HTTP_200_OK
        )

    def delete(self, request):
        person: Person = self.request.user.person
        person.avatar.delete()
        person.save()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class UserUpdateView(generics.UpdateAPIView,
                     viewsets.ViewSetMixin):
    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        object_ = queryset.get(pk=self.request.user.id)
        self.check_object_permissions(self.request, object_)

        return object_

    def update(self, request, *args, **kwargs):
        user = request.user

        serializer = self.get_serializer(
            user,
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        self.perform_update(serializer)

        return super(UserUpdateView, self).update(request, *args, **kwargs)


class IssueListUpdateApiView(UpdateAPIView):
    """
    Bulk update issues ordering, doesn't matter is it a Backlog
    or Sprint or Agile Board.
    """
    schema = IssueListUpdateSchema()
    serializer_class = IssueChildOrderingSerializer
    http_method_names = ['put', 'options', 'head']

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


class PasswordResetView(generics.GenericAPIView):
    """
    Password reset e-mail link is confirmed, therefore
    this resets the user's password.
    Accepts the following POST parameters: token, uid,
       new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = UserPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordResetView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'detail': _('Password has been reset with the new password.')
        })


class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Calls Django Auth SetPasswordForm save method.
    Accepts the following POST parameters: new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = UserPasswordConfirmSerializer
    permission_classes = (AllowAny,)

    @sensitive_post_parameters_m
    def dispatch(self, request, *args, **kwargs):
        return super(PasswordResetConfirmView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'detail': _('New password has been saved.')
        })
