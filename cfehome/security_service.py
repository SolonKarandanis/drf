import logging
from typing import List
from django.conf import settings
from auth.group_service import GroupService
from auth.user_service import UserService
from cart.cart_service import CartService
from products.product_service import ProductService

logger = logging.getLogger('django')

user_service = UserService()
group_service = GroupService()
cart_service = CartService()
product_service = ProductService()

User = settings.AUTH_USER_MODEL


class SecurityService:

    def __can_execute(self, method_name):
        return method_name in dir(self)

    def execute_method(self, method_name: str, *args) -> bool:
        if self.__can_execute(method_name):
            func = getattr(self, method_name)
            return func(*args)
        return False

    def is_product_mine(self, product_item_uuid: str) -> bool:
        return True

    def are_cart_items_mine(self, logged_in_user: User, cart_item_ids: List[int]) -> bool:
        result = True
        cart = cart_service.fetch_user_cart(logged_in_user)
        existing_cart_item_ids = [d.id for d in cart.cart_items.all()]
        if len(existing_cart_item_ids) == 0:
            return False
        if not set(cart_item_ids).issubset(existing_cart_item_ids):
            return False
        return result
