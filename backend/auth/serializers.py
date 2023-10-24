from rest_framework import serializers

from .validators import validate_username, validate_email
from .models import User


class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    this_is_not_real = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[validate_username])
    email = serializers.CharField(validators=[validate_email])

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'is_active',
            'created_date',
            'updated_date'
        ]
