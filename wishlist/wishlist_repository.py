import logging
from typing import List

from django.conf import settings

from products.models import Product
from wishlist.models import WishListItem

logger = logging.getLogger('django')
User = settings.AUTH_USER_MODEL


class WishListRepository:

    def fetch_user_wish_list_items(self, logged_in_user: User) -> List[WishListItem]:
        items = WishListItem.objects.get_queryset() \
            .with_product() \
            .owned_by(logged_in_user)
        return items

    def delete_wish_list_items_by_ids(self, item_ids: List[int]) -> None:
        WishListItem.objects.filter(pk__in=item_ids).delete()

    def initialize_wish_list_item(self, product: Product, user: User, attributes: str) -> WishListItem:
        return WishListItem.objects.create_wish_list_item(product, user, attributes)