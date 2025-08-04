from typing import List
from datetime import timedelta, date
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import User, UserDetails, UserManager
from django.contrib.auth.models import Group
import logging

logger = logging.getLogger('django')


class UserRepository:

    def _model_manager(self) -> UserManager:
        return User.objects

    def find_all_users(self) -> List[User]:
        return self._model_manager().all()

    def find_active_user(self, username: str) -> User | None:
        try:
            return self._model_manager().get_queryset().is_verified().is_active().get(username=username)
        except ObjectDoesNotExist:
            return None

    def find_user_groups(self, user: User) -> List[Group]:
        return user.groups.all()

    def user_email_exists(self, email: str) -> bool:
        exists = self._model_manager().filter(email=email).exists()
        return exists

    def find_user_by_username(self, username: str) -> User:
        return self._model_manager().get_queryset().with_groups().get(username=username)

    def find_user_by_email(self, email: str) -> User:
        return self._model_manager().get_queryset().with_groups().get(email=email)

    def user_username_exists(self, username: str) -> bool:
        exists = self._model_manager().filter(username=username).exists()
        return exists

    def user_user_id_exists(self, id: int) -> bool:
        exists = self._model_manager().filter(id=id).exists()
        return exists

    def find_user_by_id(self, user_id: int) -> User:
        return self._model_manager().get_queryset().with_details().with_groups().get(pk=user_id)

    def find_user_by_uuid_with_relations(self, uuid: str) -> User:
        return self._model_manager().get_queryset().with_details().with_groups().get(uuid=uuid)

    def find_user_by_uuid(self, uuid: str) -> User:
        return self._model_manager().get(uuid=uuid)

    def search(self, request, logged_user: User):
        user_fields_map = {
            "id": "id",
            "username": "username",
            "firstName": "first_name",
            "lastName": "last_name",
            "email": "email",
            "createdDate": "created_date",
            "updatedDate": "updated_date"
        }
        user_filter = Q()
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

        search_filter = self._model_manager().filter(user_filter)

        if "sortField" in paging:
            sort_field = paging["sortField"]
            user_model_field_to_sort = user_fields_map.get(sort_field)
            if hasattr(User, user_model_field_to_sort):
                if "sortOrder" in paging:
                    sort_order = paging["sortOrder"]
                    if sort_order == "DESC":
                        user_model_field_to_sort = f'-{user_model_field_to_sort}'
            return search_filter.order_by(user_model_field_to_sort)
        return search_filter

    def update_user(self, user: User) -> User:
        return self._model_manager().update_user(user)

    def update_user_fields(self, user: User, fields: List[str]) -> User:
        return user.save(update_fields=fields)

    def remove_unverified_users(self, days: int) -> None:
        users = self._model_manager().filter(is_verified=False)
        today = date.today()

        for x in users:
            start_date = x.created_date.date()
            end_date = start_date + timedelta(days=days)
            if end_date < today:
                self._model_manager().get(pk=x.id).delete()
                logger.info(f'Just deleted  {x.username}')

    def user_details_user_id_exists(self, id: int) -> bool:
        return UserDetails.objects.filter(user_id=id).exists()

    def find_user_details_by_user_id(self, id: int) -> UserDetails:
        try:
            return UserDetails.objects.get(user_id=id)
        except UserDetails.DoesNotExist:
            return None

    def create_user_details(self, id: int) -> UserDetails:
        details = UserDetails.objects.create(user_id=id)
        return details

    def update_user_details(self, user_details: UserDetails) -> UserDetails:
        return UserDetails.objects.update_details(user_details)

    def create_user(self, email: str, password: str, **extra_fields) -> User:
        return self._model_manager().create_user(email, password, **extra_fields)

    def create_superuser(self, email: str, password: str, **extra_fields) -> User:
        return self._model_manager().create_superuser(email, password, **extra_fields)
