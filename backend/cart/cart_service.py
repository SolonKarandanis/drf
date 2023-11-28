from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from .models import Cart
from .cart_repository import CartRepository
from products.product_repository import ProductRepository

import logging

cart_repo = CartRepository()
product_repo = ProductRepository()

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

    @transaction.atomic
    def add_to_cart(self, serialized_data):
        data_list = [dict(item) for item in serialized_data]
        product_ids = [d['product_id'] for d in data_list]
        products_to_be_added = product_repo.find_products_by_ids(product_ids)
        product_quantities_dict = {d['product_id']: d['quantity'] for d in data_list}
