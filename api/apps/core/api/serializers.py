from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.forms import Form
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt import serializers as serializers_jwt

from ..models import *


class TokenObtainPairExtendedSerializer(serializers_jwt.TokenObtainPairSerializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def validate(self, attrs):
        data = super(TokenObtainPairExtendedSerializer, self).validate(attrs)

        latency_reduced_timestamp = timezone.now() - settings.REQUEST_LATENCY

        access_token_expired_at = latency_reduced_timestamp + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']
        refresh_token_expired_at = latency_reduced_timestamp + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']

        data.update({
            'email': self.user.username,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'access_expired_at': access_token_expired_at,
            'refresh_expired_at': refresh_token_expired_at,
        })

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


"""
@todo
Class Password Reset Serializer
Look at: https://github.com/Tivix/django-rest-auth/blob/master/rest_auth/serializers.py
"""


"""
@todo
Class Password Reset Confirm Serializer
Look at: https://github.com/Tivix/django-rest-auth/blob/master/rest_auth/serializers.py 
"""


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


class ProjectBacklogSerializer(WorkspaceModelSerializer):
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
