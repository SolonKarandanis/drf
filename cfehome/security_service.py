import logging

from auth.group_service import GroupService
from auth.user_service import UserService
from cart.cart_service import CartService

logger = logging.getLogger('django')

user_service = UserService()
group_service = GroupService()
cart_service = CartService()

class SecurityService:
    pass