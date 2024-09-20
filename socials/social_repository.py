from typing import List

from cfehome import settings
from socials.models import SocialUser

User = settings.AUTH_USER_MODEL


class SocialRepository:

    def find_users_socials(self, user_id: int) -> List[SocialUser]:
        return SocialUser.objects.prefetch_related('social').filter(user_id=user_id)

    def create_user_social(self, social_user: SocialUser) -> None:
        social_user.save()

    def create_user_socials(self, social_user_list: List[SocialUser]) -> None:
        SocialUser.objects.bulk_create(social_user_list)

    def delete_user_social(self, id: int) -> None:
        SocialUser.objects.filter(id=id).delete()

    def delete_user_socials(self, id_list: List[int]) -> None:
        social_users = SocialUser.objects.filter(id__in=id_list)
        social_users.delete()

    def exists_by_user_id_and_social_id(self, user_id: int, social_id: int) -> bool:
        return SocialUser.object.filter(user_id=user_id, social_id=social_id).exists()
