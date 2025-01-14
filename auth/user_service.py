import logging
from typing import List, Dict
from rest_framework import serializers
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.utils import timezone

from cfehome.constants.security_constants import ADMIN_ID, ADMIN
from cfehome.utils.user_util import UserUtil
from images.image_repository import ImageRepository
from images.models import Images
from .group_repository import GroupRepository
from .serializers import UploadProfilePictureSerializer, UpdateBioSerializer, UpldateUserContactInfoSerializer, \
    CreateUserSerializer, ResetUserPasswordSerializer
from .user_repository import UserRepository
from .models import User, UserStatus, UserDetails

repo = UserRepository()
image_repo = ImageRepository()
groupRepo = GroupRepository()

logger = logging.getLogger('django')


class UserService:

    def find_all_users(self) -> List[User]:
        return repo.find_all_users()

    def find_active_user(self, username: str) -> User:
        return repo.find_active_user(username)

    def user_username_exists(self, username: str) -> bool:
        return repo.user_username_exists(username)

    def find_user_by_username(self, username: str) -> User:
        return repo.find_user_by_username(username)

    def user_email_exists(self, email: str) -> bool:
        return repo.user_email_exists(email)

    def find_user_by_id(self, user_id: int) -> User:
        return repo.find_user_by_id(user_id)

    def find_user_by_uuid(self, uuid: str, fetch_relations: bool = False) -> User:
        if fetch_relations:
            return repo.find_user_by_uuid_with_relations(uuid)
        return repo.find_user_by_uuid(uuid)

    def search(self, request, logged_user: User):
        return repo.search(request, logged_user)

    @transaction.atomic
    def change_user_account_status(self, status: str, user_uuid: str) -> None:
        user: User = self.find_user_by_uuid(user_uuid)
        is_admin = UserUtil.has_role(user, ADMIN)

        if not is_admin:
            raise serializers.ValidationError({"not-allowed": "Action not allowed."})

        user.status = status
        if UserStatus.ACTIVE.__eq__(status):
            user.is_active = True
            user.is_verified = True
        elif UserStatus.UNVERIFIED.__eq__(status):
            user.is_verified = False
        elif UserStatus.DEACTIVATED.__eq__(status) or UserStatus.DELETED.__eq__(status):
            user.is_active = False
        self.update_user(user)

    def user_account_status_activated(self, uuid: str) -> None:
        status = UserStatus.ACTIVE
        self.change_user_account_status(status, uuid)

    def user_account_status_deactivated(self, uuid: str) -> None:
        status = UserStatus.DEACTIVATED
        self.change_user_account_status(status, uuid)

    def user_account_status_deleted(self, uuid: str) -> None:
        status = UserStatus.DELETED
        self.change_user_account_status(status, uuid)

    def update_user(self, user: User) -> User:
        return repo.update_user(user)

    @transaction.atomic
    def update_user_contact_info(self, uuid: str, request: UpldateUserContactInfoSerializer) -> User:
        user = self.find_user_by_uuid(uuid)
        if user is None:
            raise serializers.ValidationError(f"User does not exist")
        serialized_data = request.data
        data_dict = dict(serialized_data)

        details = repo.find_user_details_by_user_id(user.id)
        if details is None:
            details = repo.create_user_details(user.id)

        if "email" in data_dict:
            email = data_dict['email']
            self.check_email_validity(email, user.email)
            user.email = email
        if "phone" in data_dict:
            phone = data_dict['phone']
            details.phone = phone
        if "country" in data_dict:
            country = data_dict['country']
            details.country = country
        if "state" in data_dict:
            state = data_dict['state']
            details.state = state
        if "city" in data_dict:
            city = data_dict['city']
            details.city = city
        if "address" in data_dict:
            address = data_dict['address']
            details.address = address
        if "zip" in data_dict:
            zip = data_dict['zip']
            details.zip = zip
        repo.update_user(user)
        repo.update_user_details(details)
        return self.find_user_by_uuid(uuid)

    def check_email_validity(self, email: str, existing_user_email: str) -> None:
        if email != existing_user_email:
            email_exists = repo.user_email_exists(email=email)
            if email_exists:
                raise serializers.ValidationError(f"Email: {email} already exists")

    @transaction.atomic
    def update_user_bio(self, uuid: str, request: UpdateBioSerializer) -> User:
        user = self.find_user_by_uuid(uuid)
        if user is None:
            raise serializers.ValidationError(f"User does not exist")

        serialized_data = request.data
        data_dict = dict(serialized_data)
        bio = data_dict['bio']
        user.bio = bio
        repo.update_user_fields(user, ['bio'])
        return self.find_user_by_uuid(uuid)

    @transaction.atomic
    def upload_cv(self, cv: InMemoryUploadedFile, uuid: str) -> None:
        user: User = repo.find_user_by_uuid(uuid)
        logger.info(f'cv: {cv}')
        user.cv = cv
        user.uploaded_at = timezone.now().date()
        repo.update_user_fields(user, ['cv', 'uploaded_at'])

    @transaction.atomic
    def upload_profile_image(self, image: InMemoryUploadedFile, request: UploadProfilePictureSerializer,
                             logged_in_user: User) -> None:

        existing_image: Images = image_repo.find_profile_image(logged_in_user.id)
        if existing_image is not None:
            existing_image.is_profile_image = False
            image_repo.update_image_is_profile_image(existing_image)

        serialized_data = request.data
        data_dict = dict(serialized_data)
        title = data_dict['title']
        alt = data_dict['alt']
        image_repo.upload_profile_image(image, title, alt, logged_in_user, logged_in_user)

    def get_user_statuses(self) -> Dict[str, str]:
        user_statuses = {
            "ACTIVE": "Active",
            "UNVERIFIED": "Unverified",
            "DEACTIVATED": "Deactivated",
            "DELETED": "Deleted"
        }
        return user_statuses

    @transaction.atomic
    def get_user_image(self, uuid: str) -> Images:
        user: User = repo.find_user_by_uuid(uuid)
        user_image = image_repo.find_profile_image(user.id)
        logger.info(f'user_image: {user_image}')
        return user_image

    def create_user(self, role: int, email: str, password: str, **extra_fields) -> User:
        if role == ADMIN_ID:
            return repo.create_superuser(email, password, **extra_fields)
        return repo.create_user(email, password, **extra_fields)

    @transaction.atomic
    def register_user(self, request: CreateUserSerializer) -> User:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        username = data_dict['username']
        email = data_dict['email']
        first_name = data_dict['firstName']
        last_name = data_dict['lastName']
        password = data_dict['password']
        confirm_password = data_dict['confirmPassword']
        role = int(data_dict['role'])

        if password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user: User = self.create_user(role, email, password, username=username, first_name=first_name,
                                      last_name=last_name)
        group = groupRepo.find_by_id(role)
        user.groups.add(group)
        return user

    @transaction.atomic
    def reset_password(self, request: ResetUserPasswordSerializer, logged_in_user: User) -> None:
        serialized_data = request.data
        data_dict = dict(serialized_data)
        email = data_dict['email']
        new_password = data_dict['newPassword']
        confirm_password = data_dict['confirmPassword']

        user = repo.find_user_by_email(email)
        is_admin = UserUtil.has_role(user, ADMIN)

        if not is_admin and (user.id != logged_in_user.id):
            raise serializers.ValidationError({"not-allowed": "Action not allowed."})

        if new_password != confirm_password:
            raise serializers.ValidationError({'password': 'Passwords must match.'})

        user.set_password(new_password)
        repo.update_user_fields(user, ["password"])
