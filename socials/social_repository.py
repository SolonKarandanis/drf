from typing import List

from cfehome import settings
from socials.models import SocialUser

User = settings.AUTH_USER_MODEL


class SocialRepository:
    def find_users_socials(self, user_id: int) -> List[SocialUser]:
        return SocialUser.objects.prefetch_related('social').filter(user_id=user_id)
