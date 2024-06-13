from typing import List
from datetime import timedelta, date
from django.db.models import Q
from .models import User
import logging

logger = logging.getLogger('django')


class UserRepository:

    def find_all_users(self) -> List[User]:
        return User.objects.all()

    def user_email_exists(self, email: str) -> bool:
        exists = User.objects.filter(email=email).exists()
        return exists

    def find_user_by_username(self, username: str) -> User:
        return User.objects.get_queryset().with_groups().get(username=username)

    def user_username_exists(self, username: str) -> bool:
        exists = User.objects.filter(username=username).exists()
        return exists

    def find_user_by_id(self, user_id: int) -> User:
        # socials = Prefetch('socialuser_set', queryset=Social.objects.filter(social__socialuser__user=advisor))
        return User.objects.get_queryset().with_details().with_groups().get(pk=user_id)

    def find_user_by_uuid_with_relations(self, uuid: str) -> User:
        return User.objects.get_queryset().with_details().with_groups().get(uuid=uuid)

    def find_user_by_uuid(self, uuid: str) -> User:
        return User.objects.get(uuid=uuid)

    def search(self, request, logged_user: User):
        user_manager = User.objects
        user_filter = Q(is_active=True) & Q(is_verified=True)
        paging = request["paging"]
        isAdmin = logged_user.is_staff

        if "name" in request:
            name: str = request["name"]
            if len(name.strip()) != 0:
                user_filter.add(
                    Q(
                        Q(first_name__icontains=name) | Q(last_name__icontains=name)
                    ),
                    Q.OR
                )
        if "email" in request:
            email: str = request["email"]
            if len(email.strip()) != 0:
                user_filter.add(Q(email__icontains=email), Q.AND)

        if "username" in request:
            username: str = request["username"]
            if len(username.strip()) != 0:
                user_filter.add(Q(username__icontains=username), Q.AND)

        if "role" in request:
            role: int = request["role"]
            if role and role > 0:
                user_filter.add(Q(groups=role), Q.AND)

        if "status" in request:
            status: str = request["status"]
            if len(status.strip()) != 0:
                user_filter.add(Q(status=status), Q.AND)

        if not isAdmin:
            user_filter.add(Q(is_verified=True) & Q(is_active=True), Q.AND)

        search_filter = user_manager.filter(user_filter)

        if "sortField" in paging:
            sortField = paging["sortField"]
            if hasattr(User, sortField):
                if "sortOrder" in paging:
                    sortOrder = paging["sortOrder"]
                    if sortOrder == "DESC":
                        sortField = f'-{sortField}'
            return search_filter.order_by(sortField)
        return search_filter

    def update_user(self, user: User) -> User:
        return User.objects.update_user(user)

    def update_user_fields(self, user: User, fields: List[str]) -> User:
        return user.save(update_fields=fields)

    def remove_unverified_users(self, days: int) -> None:
        users = User.objects.filter(is_verified=False)
        today = date.today()

        for x in users:
            start_date = x.created_date.date()
            end_date = start_date + timedelta(days=days)
            if end_date < today:
                User.objects.get(pk=x.id).delete()
                logger.info(f'Just deleted  {x.username}')
