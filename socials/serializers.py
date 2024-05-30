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
    socialName = serializers.SerializerMethodField(method_name='get_social_name')
    socialIcon = serializers.SerializerMethodField(method_name='get_social_icon')

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

    def get_social_name(self, obj):
        return obj.social.name

    def get_social_icon(self, obj):
        return obj.social.icon