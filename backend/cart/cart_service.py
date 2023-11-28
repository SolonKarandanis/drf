from django.conf import settings
from django.core.cache import cache
from .models import Cart
from .cart_repository import CartRepository
import logging

cart_repo = CartRepository()

User = settings.AUTH_USER_MODEL

logger = logging.getLogger('django')

class CartService:

    def fetch_user_cart(self, logged_in_user: User) -> Cart:
        user_id = logged_in_user.id
        cache_key = f'cart-{user_id}'
        cart = cache.get(cache_key)
        if cart is None:
            cart = Cart.objects.get_queryset() \
                .with_cart_items() \
                .owned_by(logged_in_user)
            cache.set(cache_key, cart, timeout=120)
        logger.info(f'cart: {cart}')
        return cart