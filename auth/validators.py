from django.contrib.auth.models import Group
from rest_framework import serializers
from .group_repository import GroupRepository
from .user_repository import UserRepository
from .models import User
groupRepo = GroupRepository()
userRepo = UserRepository()


def validate_username(self):
    qs = userRepo.user_username_exists(username=self)
    if qs:
        raise serializers.ValidationError(f"Username: {self} already exists")
    return self


def validate_email(self):
    qs = userRepo.user_email_exists(email=self)
    if qs:
        raise serializers.ValidationError(f"Email: {self} already exists")
    return self


def validate_role(self):
    qs = groupRepo.exists_by_name(name=self)
    if not qs:
        raise serializers.ValidationError(f"Role: {self} does not exist")
    return self
