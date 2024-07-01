import logging
from typing import List

from auth.user_repository import UserRepository
from cfehome import settings
from socials.models import SocialUser
from socials.social_repository import SocialRepository

User = settings.AUTH_USER_MODEL

repo = SocialRepository()
user_repo = UserRepository()
logger = logging.getLogger('django')


class SocialService:
    def find_users_socials(self, uuid: str) -> List[SocialUser]:
        user = user_repo.find_user_by_uuid(uuid)
        return repo.find_users_socials(user.id)
