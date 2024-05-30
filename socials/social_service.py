import logging
from typing import List

from cfehome import settings
from socials.models import SocialUser
from socials.social_repository import SocialRepository

User = settings.AUTH_USER_MODEL

repo = SocialRepository()
logger = logging.getLogger('django')


class SocialService:
    def find_users_socials(self, user_id: int) -> List[SocialUser]:
        return repo.find_users_socials(user_id)
