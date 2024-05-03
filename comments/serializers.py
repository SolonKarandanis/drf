from rest_framework import serializers
from .models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'id',
            'content',
            'content_type',
            'object_id',
            'date_created',
            'user_id',
            'user_username',
            'user_email',
        ]
