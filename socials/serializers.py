from rest_framework import serializers

from socials.models import SocialUser, Social


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = [
            'name',
            'icon',
        ]


class SocialUserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id', read_only=True)
    socialId = serializers.IntegerField(source='social_id', read_only=True)
    socialName = serializers.CharField(source="social__name")
    socialIcon = serializers.CharField(source="social__icon")

    class Meta:
        model = SocialUser
        fields = [
            'id',
            'userId',
            'socialId',
            'url',
            'socialName',
            'socialIcon'
        ]
