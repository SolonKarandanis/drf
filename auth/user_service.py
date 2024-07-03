import logging
from typing import List, Dict

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction
from django.utils import timezone

from images.image_repository import ImageRepository
from .serializers import UploadProfilePictureSerializer
from .user_repository import UserRepository
from .models import User, UserStatus

repo = UserRepository()
image_repo = ImageRepository()

logger = logging.getLogger('django')


class UserService:

    def find_all_users(self) -> List[User]:
        return repo.find_all_users()

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
    def upload_cv(self, cv: InMemoryUploadedFile, uuid: str) -> None:
        user: User = repo.find_user_by_uuid(uuid)
        logger.info(f'cv: {cv}')
        user.cv = cv
        user.uploaded_at = timezone.now().date()
        repo.update_user_fields(user, ['cv', 'uploaded_at'])

    @transaction.atomic
    def upload_profile_image(self, image: InMemoryUploadedFile, request: UploadProfilePictureSerializer, uuid: str,
                             logged_in_user: User) -> None:
        user: User = repo.find_user_by_uuid(uuid)
        serialized_data = request.data
        data_dict = dict(serialized_data)
        title = data_dict['title']
        alt = data_dict['alt']
        image_repo.upload_profile_image(image, title, alt, user, logged_in_user)

    def get_user_statuses(self) -> Dict[str, str]:
        user_statuses = {
            "ACTIVE": "Active",
            "UNVERIFIED": "Unverified",
            "DEACTIVATED": "Deactivated",
            "DELETED": "Deleted"
        }
        return user_statuses

    @transaction.atomic
    def get_user_image(self, uuid: str):
        user: User = repo.find_user_by_uuid(uuid)
        user_image = image_repo.find_image_by_object_id(user.id)
        logger.info(f'user_image: {user_image}')