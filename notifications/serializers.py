from rest_framework import serializers
from .models import NotificationEvent


class NotificationEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationEvent
        fields = [
            'id',
            'event_type',
            'payload',
            'status',
            'created_at',
            'sent_at',
            'read_at',
        ]
        read_only_fields = fields


class MarkAsReadSerializer(serializers.Serializer):
    ids = serializers.ListField(child=serializers.IntegerField(), min_length=1)
