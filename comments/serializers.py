from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    contentType = serializers.CharField(source='content_type', read_only=True)
    objectId = serializers.IntegerField(source='object_id', read_only=True)
    dateCreated = serializers.DateTimeField(source='date_created', read_only=True)
    userId = serializers.IntegerField(source='user_id', read_only=True)
    username = serializers.CharField(source='user_username', read_only=True)
    userEmail = serializers.CharField(source='user_email', read_only=True)

    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'contentType',
            'objectId',
            'dateCreated',
            'userId',
            'username',
            'userEmail',
        ]
