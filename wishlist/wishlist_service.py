from typing import List

from django.conf import settings

from wishlist.models import WishListItem
from wishlist.wishlist_repository import WishListRepository

wishlist_repo = WishListRepository()
User = settings.AUTH_USER_MODEL


class WishlistService:

    def fetch_user_wish_list_items(self, logged_in_user: User) -> List[WishListItem]:
        return wishlist_repo.fetch_user_wish_list_items(logged_in_user)

    def delete_wish_list_items(self, request, logged_in_user: User) -> None:
        items = self.fetch_user_wish_list_items(logged_in_user)
