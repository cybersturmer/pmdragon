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


class PersonVerifySerializer(serializers.Serializer):
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
