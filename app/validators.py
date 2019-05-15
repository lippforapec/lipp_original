from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
import operator
import json

class TimelineSerializer(serializers.Serializer):
     date = serializers.CharField(max_length=100)
     content = serializers.CharField(max_length=2000)

class MembersSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    career = serializers.CharField(max_length=2000)

def validate_timeline(validated_data):
    serialized = TimelineSerializer(data=validated_data, many=True)
    if serialized.is_valid():
        return validated_data
    else:
        raise ValidationError(_("timeline is not a valid form"))


def validate_members(validated_data):
    serialized = MembersSerializer(data=validated_data, many=True)
    if serialized.is_valid():
        return validated_data
    else:
        raise ValidationError(_("members are not valid "))
