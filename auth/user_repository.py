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
        return User.objects.get_queryset().with_details().with_groups().get(pk=user_id)

    def find_user_by_uuid(self, uuid: str) -> User:
        return User.objects.get_queryset().with_details().with_groups().get(uuid=uuid)

    def search(self, request):
        user_filter = Q(is_active=True) & Q(is_verified=True)

        if "name" in request:
            name = request["name"]
            user_filter.add(
                Q(
                    Q(first_name__icontains=name) | Q(last_name__icontains=name)
                ),
                Q.OR
            )
        if "email" in request:
            email = request["email"]
            user_filter.add(Q(email__icontains=email), Q.OR)

        if "username" in request:
            username = request["username"]
            user_filter.add(Q(username__icontains=username), Q.OR)

        if "role" in request:
            role = request["role"]
            user_filter.add(Q(groups=role), Q.AND)

        query = User.objects.filter(user_filter)

        return query
