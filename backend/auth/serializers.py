from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    this_is_not_real = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)
