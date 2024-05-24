import logging

from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .group_repository import GroupRepository
from .validators import validate_username, validate_email, validate_role
from .models import User, UserDetails

groupRepo = GroupRepository()

logger = logging.getLogger('django')


class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    username = serializers.CharField(read_only=True)
    id = serializers.IntegerField(read_only=True)


class UserIdSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)


class UserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isActive = serializers.CharField(source="is_active")
    isStaff = serializers.CharField(source="is_staff")
    isVerified = serializers.CharField(source="is_verified")
    createdDate = serializers.CharField(source="created_date")
    updatedDate = serializers.CharField(source="updated_date")

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'firstName',
            'lastName',
            'email',
            'isActive',
            'isStaff',
            'isVerified',
            'createdDate',
            'updatedDate',
            'uuid'
        ]


class PaginatedUserSerializer:
    """
    Serializes page objects of product querysets.
    """

    def __init__(self, data, request):
        page = request.GET.get('page', 1)
        size = request.GET.get('size', 10)
        logger.info(f'page: {page}')
        logger.info(f'size: {size}')
        paginator = Paginator(data, size)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        count = paginator.count

        previous = None if not data.has_previous() else data.previous_page_number()
        next = None if not data.has_next() else data.next_page_number()
        serializer = UserSerializer(data, many=True)
        self.page_data = {'count': count, 'previous': previous, 'next': next, 'data': serializer.data}


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name')


class UserDetailSerializer(serializers.ModelSerializer):
    userId = serializers.IntegerField(source='user_id', read_only=True)

    class Meta:
        model = UserDetails
        fields = [
            'userId',
            'state',
            'city',
            'address',
            'zip',
            'phone'
        ]


class UserAccountSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    permissions = serializers.SerializerMethodField()
    details = UserDetailSerializer(source="user_details")
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isActive = serializers.CharField(source="is_active")
    isStaff = serializers.CharField(source="is_staff")
    isVerified = serializers.CharField(source="is_verified")
    createdDate = serializers.CharField(source="created_date")
    updatedDate = serializers.CharField(source="updated_date")

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'firstName',
            'lastName',
            'email',
            'isActive',
            'isStaff',
            'isVerified',
            'status',
            'createdDate',
            'updatedDate',
            'uuid',
            'groups',
            'permissions',
            'details'
        ]

    def get_permissions(self, obj):
        return obj.get_group_permissions()


class UseInfoSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)
    permissions = serializers.SerializerMethodField()
    details = UserDetailSerializer(source="user_details")
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    isActive = serializers.CharField(source="is_active")
    isStaff = serializers.CharField(source="is_staff")
    isVerified = serializers.CharField(source="is_verified")
    createdDate = serializers.CharField(source="created_date")
    updatedDate = serializers.CharField(source="updated_date")

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'firstName',
            'lastName',
            'email',
            'isActive',
            'isStaff',
            'isVerified',
            'status',
            'createdDate',
            'updatedDate',
            'bio',
            'uuid',
            'groups',
            'permissions',
            'details'
        ]

    def get_permissions(self, obj):
        return obj.get_group_permissions()


class CreateUserSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    username = serializers.CharField(validators=[validate_username])
    email = serializers.CharField(validators=[validate_email])
    password2 = serializers.CharField(write_only=True)
    role = serializers.CharField(validators=[validate_role])

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'password2',
            'firstName',
            'lastName',
            'email',
            'role',
        ]

    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        last_name = self.validated_data['last_name']
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        role = self.validated_data['role']
        user = User(username=username, email=email, first_name=first_name, last_name=last_name)

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords must match.'})
        user.set_password(password)
        group = groupRepo.find_by_name(role)
        user.save()
        user.groups.add(group)
        return user


class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(style={"input_type": "password"}, required=True)
    new_password = serializers.CharField(style={"input_type": "password"}, required=True)

    def validate_current_password(self, value):
        if not self.context['request'].user.check_password(value):
            raise serializers.ValidationError({'current_password': 'Does not match'})
        return value
