from typing import List

from .models import User

class UserRepository:

    def find_all_users(self) -> List[User]:
        return User.objects.all()

    def user_email_exists(self, email: str) -> bool:
        exists = User.objects.filter(email=email).exists()
        return exists

    def user_username_exists(self, username: str) -> bool:
        exists = User.objects.filter(username=username).exists()
        return exists