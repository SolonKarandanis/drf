from rest_framework import serializers
from .models import User


def validate_username(self, value):
    qs = User.objects.filter(username=value)
    if qs.exists():
        raise serializers.ValidationError(f"Username: {value} already exists")
    return value


def validate_email(self, value):
    qs = User.objects.filter(email=value)
    if qs.exists():
        raise serializers.ValidationError(f"Email: {value} already exists")
    return value
