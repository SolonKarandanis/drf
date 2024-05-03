from typing import List
from django.db.models import Q

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

    def find_user_by_id(self, user_id: int) -> User:
        return User.objects.get_queryset().with_groups().get(pk=user_id)

    def search(self, params) -> List[User]:
        user_filter = Q(is_active=True)
        value = params["value"]

        if "name" in params:
            user_filter.add(
                Q(
                    Q(first_name_icontains=value) | Q(last_name_icontains=value)
                ),
                Q.OR
            )
        if "email" in params:
            user_filter.add(Q(email_icontains=value), Q.OR)

        return User.objects.filter(user_filter)
