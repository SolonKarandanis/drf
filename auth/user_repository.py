from typing import List
from django.db.models import Q, Prefetch

from socials.models import Social, SocialUser
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
        user = User.objects.get_queryset().with_details().with_groups().get(uuid=uuid)

        # socials = Social.objects.filter(socialuser__user=user)
        su = SocialUser.objects.prefetch_related('social').filter(user=user)
        # user.socialuser_set.add(su.values())
        logger.info(f'social: {su}')
        return user

    def find_user_by_uuid(self, uuid: str) -> User:
        return User.objects.get(uuid=uuid)

    def search(self, request, logged_user: User):
        user_manager = User.objects
        user_filter = Q(is_active=True) & Q(is_verified=True)
        paging = request["paging"]
        isAdmin = logged_user.is_staff

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