import logging
from typing import List

from django.conf import settings

from products.models import Product
from wishlist.models import WishListItem, WishListItemManager

logger = logging.getLogger('django')
User = settings.AUTH_USER_MODEL


class WishListRepository:

    def _model_manager(self) -> WishListItemManager:
        return WishListItem.objects

    def fetch_user_wish_list_items_with_product(self, logged_in_user: User) -> List[WishListItem]:
        items = self._model_manager().get_queryset() \
            .with_product() \
            .owned_by(logged_in_user)
        return items

    def fetch_user_wish_list_items(self, logged_in_user: User) -> List[WishListItem]:
        items = self._model_manager().get_queryset() \
            .owned_by(logged_in_user)
        return items

    def delete_wish_list_items_by_ids(self, item_ids: List[int]) -> None:
        self._model_manager().filter(pk__in=item_ids).delete()

    def initialize_wish_list_item(self, product: Product, user: User, attributes: str) -> WishListItem:
        return self._model_manager().create_wish_list_item(product, user, attributes)

    def exists_by_user_and_product_and_attributes(self, product: Product, logged_in_user: User,
                                                  attributes: str) -> bool:
        return self._model_manager().get_queryset() \
            .owned_by(logged_in_user) \
            .filter(product=product) \
            .filter(attributes=attributes) \
            .exists()

    def create_wishlist_items(self, items: List[WishListItem]) -> None:
        return self._model_manager().bulk_create(items)
