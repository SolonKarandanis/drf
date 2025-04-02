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

    def execute_method(self, method_name: str, **kwargs) -> bool:
        if self.__can_execute(method_name):
            func = getattr(self, method_name)
            return func(**kwargs)
        return False

    def is_user_me(self, **kwargs) -> bool:
        result = True
        request_uuid = str(kwargs.get('uuid'))
        logged_in_user: User = kwargs.get('logged_in_user')
        logged_in__user_uuid = str(logged_in_user.uuid)
        if request_uuid != logged_in__user_uuid:
            result = False
        return result

    def is_product_mine(self, **kwargs) -> bool:
        result = True
        existing_product = product_service.find_by_uuid(kwargs.get('uuid'), False)
        logged_in_user = kwargs.get('logged_in_user')
        is_product_mine = existing_product.user == logged_in_user
        logger.info(f'-----> is_product_mine ----> {is_product_mine=}')
        if not is_product_mine:
            result = False
        return result

    def are_cart_items_mine(self, **kwargs) -> bool:
        result = True
        logger.info(f'----->is_user_me----> request kwargs {kwargs}')
        logged_in_user = kwargs.get('logged_in_user')
        cart_item_ids = kwargs.get('arg')
        cart = cart_service.fetch_user_cart(logged_in_user)
        existing_cart_item_ids = [d.id for d in cart.cart_items.all()]
        if len(existing_cart_item_ids) == 0:
            return False
        if not set(cart_item_ids).issubset(existing_cart_item_ids):
            return False
        return result
