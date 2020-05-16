from rest_framework import serializers

from ..models import *


class PersonRegistrationRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = PersonRegistrationRequest
        fields = ['email', 'prefix_url']


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'created_at']

    def create(self, validated_data):
        obj = super(PersonSerializer, self).create(**validated_data)
