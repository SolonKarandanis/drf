from typing import List

from django.db import transaction

from .user_repository import UserRepository
from .models import User, UserStatus

repo = UserRepository()


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

    def find_user_by_uuid(self, uuid: str) -> User:
        return repo.find_user_by_uuid(uuid)

    def search(self, request):
        return repo.search(request)

    @transaction.atomic
    def change_user_account_status(self, status: str, user_uuid: str) -> None:
        user: User = self.find_user_by_uuid(user_uuid)
        user.status = status
        if UserStatus.ACTIVE.__eq__(status):
            user.is_active = True
        elif UserStatus.UNVERIFIED.__eq__(status):
            user.is_verified = False
        elif UserStatus.DEACTIVATED.__eq__(status) or UserStatus.DELETED.__eq__(status):
            user.is_active = False

        self.update_user(user)

    def update_user(self, user: User):
        return repo.update_user(user)