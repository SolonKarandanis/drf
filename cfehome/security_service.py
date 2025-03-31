import logging
from typing import List

from auth.group_service import GroupService
from auth.user_service import UserService
from cart.cart_service import CartService
from products.product_service import ProductService

logger = logging.getLogger('django')

user_service = UserService()
group_service = GroupService()
cart_service = CartService()
product_service = ProductService()


class SecurityService:

    def __can_execute(self, method_name):
        return method_name in dir(self)

    def is_product_mine(self, product_item_id: int) -> bool:
        return True

    def are_cart_items_mine(self, cart_item_ids: List[int]) -> bool:
        return True


