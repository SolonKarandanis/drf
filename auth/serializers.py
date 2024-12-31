import logging
from rest_framework import serializers
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions

from .group_repository import GroupRepository
from .user_repository import UserRepository
from .validators import validate_username, validate_email, validate_role
from .models import User, UserDetails
from cfehome.serializers import PagingSerializer

groupRepo = GroupRepository()
userRepo= UserRepository()

logger = logging.getLogger('django')

USER_STATUS_LABEL_OPTIONS = {
    "user.unverified": "Unverified",
    "user.active": "Active",
    "user.deactivated": "Deactivated",
    "user.deleted": "Deleted",
}

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            request = self.context["request"]
        except KeyError:
            logger.info(f'------>LoginSerializer ------>KeyError')
        finally:
            username = attrs.get("username")
            logger.info(f'------>LoginSerializer ------>username: {username}')
            user_to_login = userRepo.find_active_user(username)
            logger.info(f'------>LoginSerializer ------> user_to_login: {user_to_login}')
            if user_to_login is None:
                error_message = "This User Profile is not active"
                error_name = "not_active_profile"
                raise exceptions.AuthenticationFailed(error_message, error_name)
            return super().validate(attrs)



class UserProductInlineSerializer(serializers.Serializer):
    url = serializers.HyperlinkedIdentityField(
        view_name='product-detail',
        lookup_field='pk',
        read_only=True
    )
    title = serializers.CharField(read_only=True)


class UserPublicSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(read_only=True)
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    email = serializers.CharField()
    uuid = serializers.CharField()


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
    statusLabel = serializers.SerializerMethodField('_get_status_label')

    def _get_status_label(self, user_object) -> str:
        status = getattr(user_object, 'status')
        return USER_STATUS_LABEL_OPTIONS[status]

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
            'statusLabel',
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
    statusLabel = serializers.SerializerMethodField('_get_status_label')

    def _get_status_label(self, user_object) -> str:
        status = getattr(user_object, 'status')
        return USER_STATUS_LABEL_OPTIONS[status]

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
            'statusLabel',
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


class CreateUserSerializer(serializers.Serializer):
    firstName = serializers.CharField(source="first_name")
    lastName = serializers.CharField(source="last_name")
    username = serializers.CharField(validators=[validate_username])
    email = serializers.CharField(validators=[validate_email])
    password = serializers.CharField()
    confirmPassword = serializers.CharField()
    role = serializers.IntegerField(validators=[validate_role])

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'confirmPassword',
            'firstName',
            'lastName',
            'email',
            'role',
        ]


class ResetUserPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(validators=[validate_email])
    newPassword = serializers.CharField(required=True)
    confirmPassword = serializers.CharField(required=True)


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
    email = serializers.CharField(required=False, allow_blank=False)
    phone = serializers.CharField(required=False, allow_blank=False)
    country = serializers.CharField(required=False, allow_blank=False)
    state = serializers.CharField(required=False, allow_blank=False)
    city = serializers.CharField(required=False, allow_blank=False)
    address = serializers.CharField(required=False, allow_blank=False)
    zip = serializers.CharField(required=False, allow_blank=False)
