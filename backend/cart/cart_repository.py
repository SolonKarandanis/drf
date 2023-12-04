from typing import List

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .models import Cart, CartItem
import logging

User = settings.AUTH_USER_MODEL

logger = logging.getLogger('django')


class CartRepository:

    def fetch_user_cart(self, logged_in_user: User) -> Cart:
        cart = Cart.objects.get_queryset() \
            .with_cart_items() \
            .owned_by(logged_in_user)
        return cart

    def update_cart(self, cart: Cart) -> Cart:
        cart = Cart.objects.update_cart(cart)
        return cart

    def update_cart_item(self, cart_item: CartItem) -> CartItem:
        item = CartItem.objects.update_cart_item(cart_item)
        return item

    def initialize_cart_item(self, quantity: int, unit_price: float, total_price: float,
                             product_id: int, cart: Cart) -> CartItem:
        return CartItem.objects.create_cart_item(quantity, unit_price, total_price, product_id, cart)
