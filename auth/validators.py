

from rest_framework import serializers
from .models import User


def validate_username(self):
    qs = User.objects.filter(username=self)
    if qs.exists():
        raise serializers.ValidationError(f"Username: {self} already exists")
    return self


def validate_email(self):
    qs = User.objects.filter(email=self)
    if qs.exists():
        raise serializers.ValidationError(f"Email: {self} already exists")
    return self
