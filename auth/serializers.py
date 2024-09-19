import logging
import uuid

from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .group_repository import GroupRepository
from .validators import validate_username, validate_email, validate_role
from .models import User, UserDetails
from cfehome.serializers import PagingSerializer

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
            'status',
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


class PaginatedPOSTUserSerializer:
    """
    Serializes page objects of product querysets.
    """

    def __init__(self, data, paging):
        limit = paging["limit"]
        page = paging["page"]
        logger.info(f'page: {page}')
        logger.info(f'size: {limit}')
        paginator = Paginator(data, limit)
        try:
            data = paginator.page(page)
        except PageNotAnInteger:
            data = paginator.page(1)
        except EmptyPage:
            data = paginator.page(paginator.num_pages)
        count = paginator.count
        pages = paginator.num_pages

        previous = None if not data.has_previous() else data.previous_page_number()
        next = None if not data.has_next() else data.next_page_number()
        serializer = UserSerializer(data, many=True)
        self.page_data = {'count': count, 'pages': pages, 'previous': previous, 'next': next, 'data': serializer.data}


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
            'country',
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
    role = serializers.IntegerField(validators=[validate_role])

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
        user.uuid = uuid.uuid4()
        group = groupRepo.find_by_id(role)
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


class SearchUsersRequestSerializer(serializers.Serializer):
    USER_STATUS_CHOICES = [
        "user.unverified",
        "user.active",
        "user.deactivated",
        "user.deleted"
    ]

    username = serializers.CharField(required=False, allow_blank=True)
    name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.CharField(required=False, allow_blank=True)
    role = serializers.IntegerField(required=True)
    status = serializers.ChoiceField(choices=USER_STATUS_CHOICES, required=False)
    paging = PagingSerializer(required=True)


class ChangeUserStatusSerializer(serializers.Serializer):
    userId = serializers.CharField(required=True)


class UploadCVSerializer(serializers.Serializer):
    cv = serializers.FileField()


class UploadProfilePictureSerializer(serializers.Serializer):
    image = serializers.ImageField()
    title = serializers.CharField(required=True)
    alt = serializers.CharField(required=False)


class UpdateBioSerializer(serializers.Serializer):
    bio = serializers.CharField(required=True, allow_blank=True)


class UpldateUserContactInfoSerializer(serializers.Serializer):
    email = serializers.CharField(validators=[validate_email])
    phone = serializers.CharField(required=False, allow_blank=False)
    country = serializers.CharField(required=False, allow_blank=False)
    state = serializers.CharField(required=False, allow_blank=False)
    city = serializers.CharField(required=False, allow_blank=False)
    address = serializers.CharField(required=False, allow_blank=False)
    zip = serializers.CharField(required=False, allow_blank=False)
