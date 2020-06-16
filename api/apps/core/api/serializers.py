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
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import serializers as serializers_jwt

from ..models import *

UserModel = get_user_model()


class TokenRefreshExtendedSerializer(serializers_jwt.TokenRefreshSerializer):
    """
    Overriding Json Web Token serializer to ensure extended data.
    """

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        parent_data = super(TokenRefreshExtendedSerializer, self).validate(attrs)

        access_token = parent_data.pop('access')
        refresh_token = parent_data.pop('refresh')

        assert len(parent_data) == 0, \
            _('Some parent data was missing')

        data = {'access': access_token,
                'refresh': refresh_token}

        return data


class TokenObtainPairExtendedSerializer(serializers_jwt.TokenObtainPairSerializer):
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
            'username': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'tokens': {
                'access': access_token,
                'refresh': refresh_token,
            },
        }

        return data


class PersonRegistrationRequestSerializer(serializers.ModelSerializer):
    """
    Common Serializer for Person Registration Request
    For creating requests.
    """

    class Meta:
        model = PersonRegistrationRequest
        fields = ['id', 'email', 'prefix_url']


class UserSetPasswordSerializer(serializers.Serializer):
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

        return attrs

    def save(self, **kwargs):
        self.set_password_form.save()
        from django.contrib.auth import update_session_auth_hash
        update_session_auth_hash(self.request, self.user)


class UserPasswordResetSerializer(serializers.Serializer):
    """
    Some serializer for request a password reset email
    """
    email = serializers.EmailField()

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


class PersonVerifySerializer(serializers.Serializer):
    """
    Custom Serializer for verifying Person registration
    For creating Person after confirmation of authenticity of email
    """
    key = serializers.CharField(max_length=128, write_only=True)
    password = serializers.CharField(max_length=30, write_only=True)

    class Meta:
        fields = ['key', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'key': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data['password']
        key = validated_data['key']

        try:
            request = PersonRegistrationRequest.valid.filter(key__exact=key).get()

        except PersonRegistrationRequest.DoesNotExist as ne:
            raise serializers.ValidationError(_('Request for registration was expired or not correct'))

        email = request.email

        """
        Person foreign key user not visible for user.
        Used for SaaS service
        """
        user = User(username=email, email=email)
        user.set_password(password)

        try:
            user.save()

        except IntegrityError:
            raise serializers.ValidationError(_('Someone already registered with this data'))

        person = Person(user=user)
        person.save()

        return person

    def update(self, instance, validated_data):
        pass


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'is_active',
            'created_at'
        ]


class WorkspaceSerializer(serializers.ModelSerializer):
    participants = PersonSerializer(many=True)

    """
    For getting information about all persons participated in workspace.
    We can get information just from the spaces we belong.
    """

    class Meta:
        model = Workspace
        fields = [
            'id',
            'prefix_url',
            'participants'
        ]


class WorkspaceModelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        validated_data = super(WorkspaceModelSerializer, self).validate(attrs)
        validated_data['workspace'] = self.context['workspace']

        return validated_data


class ProjectSerializer(WorkspaceModelSerializer):
    """
    Common project serializer
    For getting list of projects in workspace
    """

    class Meta:
        model = Project
        fields = ['id', 'title', 'key']


class IssueTypeCategorySerializer(WorkspaceModelSerializer):
    """
    Common issue category serializer
    For getting all types of issues
    """

    class Meta:
        model = IssueTypeCategory
        fields = ['id', 'title', 'is_subtask', 'ordering']


class IssueStateCategorySerializer(WorkspaceModelSerializer):
    """
    Common issue category serializer
    For getting all types of issue states
    """

    class Meta:
        model = IssueStateCategory
        fields = ['id', 'title', 'ordering']


class IssueSerializer(WorkspaceModelSerializer):
    """
    Common issue serializer for getting all tasks
    No idea how to use it in reality yet
    """

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'project',
            'type_category',
            'state_category',
            'created_by',
            'created_at',
            'ordering',
        ]


class ProjectBacklogIssuesSerializer(WorkspaceModelSerializer):
    """
    Gathering all information about issues for a Backlog serializer
    For getting issues information in Backlog Serializer
    Not for using separately
    """

    class Meta:
        model = Issue
        fields = [
            'id',
            'title',
            'project',
            'type_category',
            'state_category',
            'created_by',
            'created_at',
            'ordering'
        ]


class ProjectBacklogReadOnlySerializer(WorkspaceModelSerializer):
    """
    Getting Backlog information with all issues inside of it
    For getting backlog information including issues
    """
    class Meta:
        model = ProjectBacklog
        fields = [
            'id',
            'project_id',
            'issues',
        ]
        depth = 1


class ProjectBacklogWritableSerializer(WorkspaceModelSerializer):
    class Meta:
        model = ProjectBacklog
        fields = [
            'id',
            'project_id',
            'issues'
        ]


class SprintDurationSerializer(WorkspaceModelSerializer):
    """
    Getting Sprint Duration Variant
    """

    class Meta:
        model = SprintDuration
        fields = [
            'id',
            'title',
            'duration',
        ]


class SprintSerializer(WorkspaceModelSerializer):
    """
    Common sprint data
    """

    class Meta:
        model = Sprint
        fields = [
            'id',
            'project',
            'title',
            'goal',
            'duration',
            'issues',
            'started_at',
            'finished_at'
        ]
