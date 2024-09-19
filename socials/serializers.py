from rest_framework import serializers

from socials.models import SocialUser, Social


class SocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Social
        fields = [
            'name',
            'icon',
            'button_css_class'
        ]


class SocialUserSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id', read_only=True)
    socialId = serializers.IntegerField(source='social_id', read_only=True)
    socialName = serializers.SerializerMethodField(method_name='get_social_name')
    socialIcon = serializers.SerializerMethodField(method_name='get_social_icon')
    buttonCssClass = serializers.SerializerMethodField(method_name='get_button_css_class')

    class Meta:
        model = SocialUser
        fields = [
            'id',
            'userId',
            'socialId',
            'url',
            'socialName',
            'socialIcon',
            'buttonCssClass'
        ]

    def get_social_name(self, obj):
        return obj.social.name

    def get_social_icon(self, obj):
        return obj.social.icon

    def get_button_css_class(self, obj):
        return obj.social.button_css_class


class CreateUserSocials(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id',  required=True)
    socialId = serializers.IntegerField(source='social_id',  required=True)
    url = serializers.CharField(required=True, allow_blank=True)
