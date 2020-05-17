from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers

from ..models import *


class PersonRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRegistrationRequest
        fields = ['id', 'email', 'prefix_url']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']
        extra_kwargs = {'password': {'write_only': True}}


class PersonVerifySerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Person
        fields = ['user']

    def create(self, validated_data):
        password = validated_data['user']['password']

        request_id = self.context['request_id']
        request_key = self.context['key']

        try:
            request = PersonRegistrationRequest.valid.filter(pk=request_id, key__exact=request_key).get()

        except PersonRegistrationRequest.DoesNotExist as ne:
            raise serializers.ValidationError(_('Request for registration was expired or not correct'))

        email = request.email
        prefix = request.prefix_url

        """
        Person foreign key user not visible for user.
        Used for SaaS service
        """
        user = User(username=f"{prefix}_dragon", email=email)
        user.set_password(password)

        try:
            user.save()

        except IntegrityError as ie:
            raise serializers.ValidationError(_('Someone already registered with this data'))

        person = Person(user=user)
        person.save()

        return person
