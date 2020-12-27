from typing import Dict, Any

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.forms import Form
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode as uid_decoder
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers, permissions
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import serializers as serializers_jwt

from ..models import *

UserModel = get_user_model()


def order_issues(validated_data):
    """
    validated_data should contain issues key.
    We use it in Backlog and Sprint serializers.
    """
    if 'issues' not in validated_data:
        return validated_data

    ordered_issues = validated_data['issues']

    for index, issue in enumerate(ordered_issues):
        issue.ordering = index
        issue.save()

        ordered_issues[index] = issue

    validated_data['issues'] = ordered_issues

    return validated_data


class TokenObtainPairExtendedSerializer(serializers_jwt.TokenObtainPairSerializer):
    """
    Extend parent class to add extra data to token.
    Currently: username, first_name, last_name
    """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name

        return token

    def validate(self, attrs):
        parent_data = super(TokenObtainPairExtendedSerializer, self).validate(attrs)

        refresh_token = parent_data.pop('refresh')
        access_token = parent_data.pop('access')

        assert len(parent_data) == 0, \
            _('Some parent data was missing')

        data = {
            'access': access_token,
            'refresh': refresh_token
        }

        return data


class PersonRegistrationRequestSerializer(serializers.ModelSerializer):
    """
    Common Serializer for Person Registration Request on Registration
    """

    class Meta:
        model = PersonRegistrationRequest
        fields = (
            'email',
            'prefix_url'
        )

    def validate_prefix_url(self, attrs):
        """
        We want to be sure that user not expect to get
        workspace with already exists prefix
        @rtype: None
        @param attrs: string
        """
        prefix_url = attrs
        workspaces_with_same_prefix = Workspace.objects.filter(prefix_url=prefix_url)
        if workspaces_with_same_prefix.exists():
            raise ValidationError(_('Workspace with given prefix already exists.'))

        return prefix_url

    def validate_email(self, attrs):
        """
        We want to be sure that user,
        that already exists will register one more time with the same email
        @param attrs: We expect to have email here
        @return:
        """

        email = attrs
        users_with_the_same_email = User.objects.filter(email=email)
        if users_with_the_same_email.exists():
            raise ValidationError(_('User with given email already exists.'))

        return email


class PersonInvitationRequestRetrieveUpdateSerializer(serializers.ModelSerializer):
    """
    Update request after getting email and follow link inside
    """

    class Meta:
        model = PersonInvitationRequest
        fields = (
            'email',
            'workspace',
            'is_accepted'
        )
        extra_kwargs = {
            'email': {'read_only': True},
            'workspace': {'read_only': True},
            'is_accepted': {'write_only': True}
        }
        depth = 1

    def update(self, instance, validated_data):
        is_accepted = validated_data.get('is_accepted', instance.is_accepted)

        try:
            user = User.objects.filter(email=instance.email).get()
        except User.MultipleObjectsReturned:
            raise ValidationError(_('Error occurred while getting person to add'))

        if is_accepted and not instance.is_accepted:
            workspace = instance.workspace
            workspace.participants.add(user.person)
            workspace.save()

            instance.is_accepted = True
            instance.save()

        return instance


class PersonInvitationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonInvitationRequest
        fields = (
            'email',
            'workspace',
            'created_at',
            'expired_at'
        )


class PersonInvitationRequestList(serializers.Serializer):
    invites = PersonInvitationRequestSerializer(many=True)

    class Meta:
        fields = (
            'invites',
        )


class UserSetPasswordSerializer(serializers.Serializer):
    """
    Serializer to update password of user.
    """

    old_password = serializers.CharField(max_length=128, write_only=True)
    new_password1 = serializers.CharField(max_length=128, write_only=True)
    new_password2 = serializers.CharField(max_length=128, write_only=True)

    set_password_form_class = SetPasswordForm

    def __init__(self, *args, **kwargs):
        super(UserSetPasswordSerializer, self).__init__(*args, **kwargs)

        self.request = self.context.get('request')
        self.user = getattr(self.request, 'user', None)
        self.set_password_form: [Form] = None

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate_old_password(self, value):
        invalid_conditions = (
            self.user,
            not self.user.check_password(value),
        )

        if all(invalid_conditions):
            error_message = _('Old one password was entered incorrectly for current user. '
                              'Please try again. ')
            raise ValidationError(error_message)

        return value

    def validate(self, attrs):
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs,
        )

        if not self.set_password_form.is_valid():
            serializers.ValidationError(self.set_password_form.errors)

        new_password1 = attrs['new_password1']
        new_password2 = attrs['new_password2']

        if new_password1 != new_password2:
            serializers.ValidationError({
                'new_password2': "Password confirmation doesn't match password"
            })

        return attrs

    def save(self, **kwargs):
        self.set_password_form.save()
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(self.request, self.user)


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Some serializer for request a password reset email
    """
    email = serializers.EmailField(max_length=128,
                                   min_length=4)

    password_reset_form_class = PasswordResetForm
    reset_form: [Form] = None

    @staticmethod
    def get_email_options():
        """
        Override this to change default email options
        """
        return {}

    def validate_email(self, value):
        self.reset_form = self.password_reset_form_class(data=self.initial_data)
        if not self.reset_form.is_valid():
            raise serializers.ValidationError(self.reset_form.errors)

        return value

    def save(self, **kwargs):
        request = self.context.get('request')
        opts = {
            'use_https': request.is_secure(),
            'from_email': getattr(settings, 'DEFAULT_FROM_EMAIL'),
            'request': request,
        }

        opts.update(self.get_email_options())
        self.reset_form.save(**opts)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class UserPasswordConfirmSerializer(serializers.Serializer):
    """
    User password Confirmation serializer.
    We dont need it yet, but will need soon. Hopefully.
    """
    user: object
    _errors: Dict[Any, Any]
    set_password_form: SetPasswordForm

    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    set_password_form_class = SetPasswordForm

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def custom_validation(self, attrs):
        pass

    def validate(self, attrs):
        self._errors = {}

        try:

            uid = force_text(uid_decoder(attrs['uid']))
            self.user = UserModel._default_manager.get(pk=uid)

        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
            raise ValidationError({'uid': [_('Invalid value')]})

        self.custom_validation(attrs)
        self.set_password_form = self.set_password_form_class(
            user=self.user, data=attrs
        )
        if not self.set_password_form.is_valid():
            raise serializers.ValidationError(self.set_password_form.errors)

        if not default_token_generator.check_token(self.user, attrs['token']):
            raise ValidationError({'token': ['Invalid value']})

        return attrs

    def save(self, **kwargs):
        return self.set_password_form.save()


class PersonRegistrationOrInvitationRequestSerializer(serializers.Serializer):
    """
    Custom Serializer for verifying Person registration
    For creating Person after confirmation of authenticity of email
    """
    key = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=30, write_only=True)
    is_invited = serializers.BooleanField(write_only=True)

    class Meta:
        fields = (
            'key',
            'password'
        )
        extra_kwargs = {
            'key': {'write_only': True},
            'password': {'write_only': True},
            'is_invited': {'write_only': True}
        }

    def create(self, validated_data):
        key = validated_data.get('key')
        password = validated_data.get('password')
        is_invited = validated_data.get('is_invited')

        """
        If person was invited than we have to search him in PersonInvitationRequests 
        else we will try to find him in PersonRegistrationRequests """
        if is_invited:
            request_with_key = PersonInvitationRequest.valid.filter(key=key)
        else:
            request_with_key = PersonRegistrationRequest.valid.filter(key=key)

        if not request_with_key.exists():
            raise serializers.ValidationError({
                'detail': _('Request for registration or invitation was expired or not correct')
            })

        request = request_with_key.get()

        """
        Check if user with the same email already exists """
        email_equal_users_count = User.objects.filter(email=request.email)
        if email_equal_users_count.exists():
            raise serializers.ValidationError({
                'detail': _('User with the same email already exists. '
                            'You can create new workspace in you account. '
                            'If you forgot you password you also can restore it')
            })

        user = User(username=request.email, email=request.email)
        user.set_password(password)

        try:
            user.save()

        except IntegrityError:
            raise serializers.ValidationError({
                'detail': _('Someone already registered with this data')
            })

        person = Person(user=user)
        person.save()

        if is_invited:
            """
            If user was invited then workspace already exists
            And we don't need to create it """
            request: PersonInvitationRequest
            workspace = request.workspace
        else:
            """
            If user is self registered with prefix_url for workspace then 
            we have to create workspace for him. """
            request: PersonRegistrationRequest
            workspace = Workspace(prefix_url=request.prefix_url)

            try:
                workspace.save()
            except IntegrityError:
                raise serializers.ValidationError({
                    'detail': _('Workspace with given prefix url was already registered.')
                })

        workspace.participants.add(person)
        workspace.save()

        return person

    def update(self, instance, validated_data):
        pass


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    We need this serializer for update base information
    about user
    """

    class Meta:
        model = UserModel
        fields = (
            'username',
            'first_name',
            'last_name'
        )


class PersonSerializer(serializers.ModelSerializer):
    """
    Common Person Serializer.
    We dont need it yet.
    But maybe we will.
    """

    class Meta:
        model = Person
        fields = (
            'id',
            'username',
            'avatar',
            'first_name',
            'last_name',
            'is_active',
            'created_at'
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'created_at': {'read_only': True},
            'is_active': {'read_only': True}
        }


class WorkspaceWritableSerializer(serializers.ModelSerializer):
    """
    For creating / editing / removing workspaces
    """

    class Meta:
        model = Workspace
        fields = (
            'id',
            'prefix_url',
            'participants'
        )

    def create(self, validated_data):
        prefix_url = validated_data.get('prefix_url')
        participants = validated_data.get('participants', None)
        person = self.context.get('person')

        workspace = Workspace(
            prefix_url=prefix_url.upper(),
            created_by=person
        )

        try:
            workspace.save()
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': _('Workspace with given prefix url was already registered.')
            })

        """
        Iteration for the list of participants ids """
        if participants:
            for person_id in participants:
                _person = Person.objects.get(pk=person_id)
                workspace.participants.add(_person)

        workspace.participants.add(person)
        workspace.save()

        return workspace


class WorkspaceDetailedSerializer(serializers.ModelSerializer):
    """
    For getting information about all persons participated in workspace.
    We can get information just from the spaces we belong.
    """
    participants = PersonSerializer(many=True)

    class Meta:
        model = Workspace
        fields = (
            'id',
            'prefix_url',
            'participants',
            'projects'
        )
        depth = 1


class WorkspaceModelSerializer(serializers.ModelSerializer):
    def validate_workspace(self, value):
        """
        Check that given workspace contains person sending request.
        """
        try:
            Workspace.objects \
                .filter(participants__in=[self.context['person']]) \
                .get(prefix_url__exact=value)

        except (KeyError, Workspace.DoesNotExist):
            raise ValidationError('Incorrect workspace given for current user')

        return value


class ProjectSerializer(WorkspaceModelSerializer):
    """
    Common project serializer
    For getting list of projects in workspace
    """

    class Meta:
        model = Project
        fields = (
            'id',
            'workspace',
            'title',
            'key'
        )

    def create(self, validated_data):
        workspace = validated_data.get('workspace')
        title = validated_data.get('title')
        key = validated_data.get('key')

        project = Project(
            workspace=workspace,
            title=title.upper(),
            key=key.upper()
        )

        try:
            project.save()
        except IntegrityError:
            raise serializers.ValidationError({
                'detail': _('Project name and key should be unique.')
            })

        return project

    def update(self, instance, validated_data):
        """
        We need just upper title and key
        Workspace cannot be changed through API so we not allow it and ignore any given workspace
        """
        title: str = validated_data.get('title')
        key: str = validated_data.get('key')

        if title:
            instance.title = title.upper()

        if key:
            instance.key = key.upper()

        instance.save()

        return instance


class IssueTypeIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueTypeCategoryIcons
        fields = (
            'prefix',
            'color'
        )


class IssueTypeSerializer(WorkspaceModelSerializer):
    """
    Common issue category serializer
    For getting all types of issues
    """
    icon = IssueTypeIconSerializer()

    class Meta:
        model = IssueTypeCategory
        fields = (
            'id',
            'workspace',
            'project',
            'title',
            'icon',
            'is_subtask',
            'ordering'
        )


class IssueStateSerializer(WorkspaceModelSerializer):
    """
    Common issue category serializer
    For getting all types of issue states
    """

    class Meta:
        model = IssueStateCategory
        fields = (
            'id',
            'workspace',
            'project',
            'title',
            'is_default',
            'is_done',
            'ordering'
        )


class IssueEstimationSerializer(WorkspaceModelSerializer):
    """
    Common issue estimation serializer
    I think we can do with it whatever we want. will see.
    """

    class Meta:
        model = IssueEstimationCategory
        fields = (
            'id',
            'workspace',
            'project',
            'title',
            'value'
        )


class IssueSerializer(WorkspaceModelSerializer):
    """
    Common issue serializer for getting all tasks
    No idea how to use it in reality yet
    """

    class Meta:
        model = Issue
        fields = (
            'id',
            'workspace',
            'project',
            'title',
            'description',
            'type_category',
            'state_category',
            'estimation_category',
            'assignee',
            'created_by',
            'created_at',
            'updated_at',
            'ordering',
        )
        extra_kwargs = {
            'created_by': {'read_only': True},
            'created_at': {'read_only': True},
            'type_category': {'required': False},
            'state_category': {'required': False},
            'estimation_category': {'required': False},
            'ordering': {'required': False}
        }

    def validate(self, attrs):
        data = super(IssueSerializer, self).validate(attrs)
        data['created_by'] = self.context['person']
        return data


class IssueMessageSerializer(WorkspaceModelSerializer):
    class Meta:
        model = IssueMessage
        fields = (
            'id',
            'issue',
            'description',
            'created_by',
            'created_at',
            'updated_at'
        )
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True}
        }

    def validate(self, attrs):
        data = super().validate(attrs)
        data['created_by'] = self.context['person']
        return data


class BacklogWritableSerializer(WorkspaceModelSerializer):
    class Meta:
        model = ProjectBacklog
        fields = (
            'id',
            'workspace',
            'project_id',
            'issues'
        )

    def update(self, instance, validated_data):
        validated_data = order_issues(validated_data)
        return super(BacklogWritableSerializer, self) \
            .update(instance, validated_data)


class SprintDurationSerializer(WorkspaceModelSerializer):
    """
    Getting Sprint Duration Variant
    """

    class Meta:
        model = SprintDuration
        fields = (
            'id',
            'workspace',
            'title',
            'duration',
        )


class SprintWritableSerializer(WorkspaceModelSerializer):
    """
    Common sprint data
    """

    class Meta:
        model = Sprint
        fields = (
            'id',
            'workspace',
            'project',
            'title',
            'goal',
            'issues',
            'is_started',
            'is_completed',
            'started_at',
            'finished_at'
        )

    def update(self, instance, validated_data):
        validated_data = order_issues(validated_data)
        return super(SprintWritableSerializer, self) \
            .update(instance, validated_data)


class IssueListSerializer(serializers.ListSerializer):
    def update(self, instance, validated_data):
        issue_mapping = {issue.id: issue
                         for issue
                         in instance}

        data_mapping = {issue['id']: issue
                        for issue
                        in validated_data}

        result = []
        for issue_id, data in data_mapping.items():
            issue = issue_mapping.get(issue_id, None)

            if issue is None:
                continue

            result.append(self.child.update(issue, validated_data))

        return result


class IssueChildOrderingSerializer(WorkspaceModelSerializer):
    def update(self, instance, validated_data):
        instance.ordering = [validated_datum['ordering']
                             for validated_datum
                             in validated_data
                             if validated_datum['id'] == instance.id].pop()
        instance.save()

        return instance

    class Meta:
        model = Issue
        fields = (
            'id',
            'ordering'
        )
        extra_kwargs = {
            'id': {'read_only': False},
        }
        list_serializer_class = IssueListSerializer
