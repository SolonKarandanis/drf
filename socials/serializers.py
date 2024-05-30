from rest_framework import serializers

from socials.models import SocialUser


class SocialUserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id', read_only=True)
    socialId = serializers.IntegerField(source='social_id', read_only=True)

    class Meta:
        model = SocialUser
        fields = [
            'id',
            'userId',
            'socialId',
            'url',
        ]