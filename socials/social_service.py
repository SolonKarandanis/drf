import logging
from typing import List

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
    def find_users_socials(self, uuid: str) -> List[SocialUser]:
        user = user_repo.find_user_by_uuid(uuid)
        return repo.find_users_socials(user.id)

    def create_user_socials(self, request: CreateUserSocials):
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        for data in data_list:
            user_id = data['userId']
            social_id = data['socialId']
            url = data['url']

            exists = repo.exists_by_user_id_and_social_id(user_id, social_id)

    def delete_user_social(self, id: int) -> None:
        pass

    def delete_user_socials(self, id_list: List[int]) -> None:
        pass