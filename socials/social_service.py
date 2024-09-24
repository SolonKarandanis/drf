import logging
from typing import List

from django.db import transaction
from rest_framework import serializers
from auth.user_repository import UserRepository
from cfehome import settings
from socials.models import SocialUser
from socials.serializers import CreateUserSocials
from socials.social_repository import SocialRepository

User = settings.AUTH_USER_MODEL

repo = SocialRepository()
user_repo = UserRepository()
logger = logging.getLogger('django')


class SocialService:

    @transaction.atomic
    def find_users_socials(self, uuid: str) -> List[SocialUser]:
        user = user_repo.find_user_by_uuid(uuid)
        return repo.find_users_socials(user.id)

    @transaction.atomic
    def create_user_socials(self, uuid: str, request: CreateUserSocials) -> List[SocialUser]:
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        items = []
        for data in data_list:
            user_id = data['userId']
            social_id = data['socialId']
            url = data['url']
            exists = repo.exists_by_user_id_and_social_id(user_id, social_id)
            if not exists:
                social_user = SocialUser(user_id=user_id, social_id=social_id, url=url)
                items.append(social_user)
        repo.create_user_socials(items)
        return self.find_users_socials(uuid)

    @transaction.atomic
    def delete_user_social(self, uuid: str, id: int) -> List[SocialUser]:
        user = user_repo.find_user_by_uuid(uuid)
        social_user = repo.find_social_user_by_id(id)
        if social_user and social_user.user != user:
            raise serializers.ValidationError(f"Action Not Allowed")
        repo.delete_user_social(id)
        return self.find_users_socials(uuid)

    @transaction.atomic
    def delete_user_socials(self, uuid: str, id_list: List[int]) -> List[SocialUser]:
        user = user_repo.find_user_by_uuid(uuid)
        social_users = repo.find_social_users_by_id_list(id_list)
        social_user_ids_set = set([s.id for s in social_users])
        provided_ids_set = set(id_list)
        common_elements = social_user_ids_set.intersection(provided_ids_set)
        repo.delete_user_socials(common_elements)
        return self.find_users_socials(uuid)

    @transaction.atomic
    def delete_all_user_socials(self, uuid: str) -> List[SocialUser]:
        user = user_repo.find_user_by_uuid(uuid)
        repo.delete_all_user_socials(user.id)
        return self.find_users_socials(uuid)
