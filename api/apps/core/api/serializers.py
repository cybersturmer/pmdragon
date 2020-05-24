from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from ..models import *


class PersonRegistrationRequestSerializer(serializers.ModelSerializer):
    """
    Common Serializer for Person Registration Request
    For creating requests.
    """
    class Meta:
        model = PersonRegistrationRequest
        fields = ['id', 'email', 'prefix_url']


class UserSerializer(serializers.ModelSerializer):
    """
    Common Serializer for getting user information
    Gonna use it for getting all participants information
    in chosen workspace.
    """
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}


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
    issues = ProjectBacklogIssuesSerializer(many=True)

    class Meta:
        model = ProjectBacklog
        fields = [
            'id',
            'issues'
        ]
