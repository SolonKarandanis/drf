from typing import List

from django.conf import settings
from django.db import transaction
from .models import Cart, CartItem
from products.models import Product
from .cart_repository import CartRepository
from products.product_repository import ProductRepository
from orders.order_repository import OrderRepository

import logging

from .serializers import AddToCart, UpdateQuantity, DeleteCartItems

cart_repo = CartRepository()
product_repo = ProductRepository()
order_repo = OrderRepository()

User = settings.AUTH_USER_MODEL
key_prefix = settings.CACHES.get('default').get('KEY_PREFIX')

logger = logging.getLogger('django')


class CartService:

    def fetch_user_cart(self, logged_in_user: User) -> Cart:
        user_id = logged_in_user.id
        cart =cart_repo.fetch_user_cart(logged_in_user)
        logger.info(f'cart: {cart}')
        return cart

    def fetch_user_cart_with_products_and_users(self, logged_in_user: User) -> Cart:
        return cart_repo.fetch_user_cart_with_products_and_users(logged_in_user)

    @transaction.atomic
    def add_to_cart(self, request: AddToCart, logged_in_user: User) -> Cart:
        cart: Cart = self.fetch_user_cart(logged_in_user)
        logger.info(
            f'---> CartService ---> add_to_cart ---> cart_items: {cart.cart_items}')
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        product_ids = [d['productId'] for d in data_list]
        products_to_be_added: List[Product] = product_repo.find_products_by_ids(product_ids)
        product_quantities_dict = {d['productId']: d['quantity'] for d in data_list}
        product_attributes_dict = {d['productId']: d['attributes'] for d in data_list}
        items = []
        for product in products_to_be_added:
            product_id = product.id
            quantity = product_quantities_dict[product_id]
            price = product.price
            product_attributes = product_attributes_dict[product_id]
            # if product_attributes is None get default attribute values for product
            existing_cart_item = self._find_existing_cart_item(product_id, cart.cart_items.all(),
                                                               product_attributes)
            if existing_cart_item is None:
                cart_item = cart_repo.initialize_cart_item(quantity, price, quantity * price, product_id, cart,
                                                           product_attributes)
                items.append(cart_item)
            else:
                new_quantity = existing_cart_item.quantity + quantity
                existing_cart_item.quantity = new_quantity
                existing_cart_item.total_price = new_quantity * price
                items.append(existing_cart_item)
        cart.cart_items.add(*items, bulk=False)
        logger.info(
            f'---> CartService ---> add_to_cart ---> items: {items}')
        cart.recalculate_cart_total_price()
        self._update_cart(cart)
        return cart

    def _find_existing_cart_item(self, product_id: int, cart_items: List[CartItem],
                                 product_attributes: str) -> CartItem | None:
        if len(cart_items) == 0:
            return None
        logger.info(
            f'---> CartService ---> add_to_cart ---> product_attributes: {product_attributes}')
        for cart_item in cart_items:
            if cart_item.attributes == product_attributes and cart_item.product_id == product_id:
                logger.info(
                    f'---> CartService ---> add_to_cart ---> cart_item2: {cart_item}')
                return cart_item
        return None


    @transaction.atomic
    def update_item_quantities(self, request: UpdateQuantity, logged_in_user: User) -> Cart:
        cart: Cart = self.fetch_user_cart(logged_in_user)
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        for data in data_list:
            quantity = data['quantity']
            cart_item_id = data['cart_item_id']
            existing_cart_item = next(filter(lambda ci: ci.id == cart_item_id, cart.cart_items.all()), None)
            if existing_cart_item is not None:
                existing_cart_item.quantity = quantity
                existing_cart_item.total_price = quantity * existing_cart_item.unit_price
                cart_repo.update_cart_item(existing_cart_item)
        cart = self.fetch_user_cart(logged_in_user)
        cart.recalculate_cart_total_price()
        self._update_cart(cart)
        return cart

    @transaction.atomic
    def delete_cart_items(self, request: DeleteCartItems, logged_in_user: User) -> Cart:
        cart: Cart = self.fetch_user_cart(logged_in_user)
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        cart_item_ids = [d['cart_item_id'] for d in data_list]
        existing_cart_items = list(filter(lambda ci: ci.id in cart_item_ids, cart.cart_items.all()))
        logger.info(f'items: {existing_cart_items}')
        if existing_cart_items is not None:
            cart.cart_items.remove(*existing_cart_items)
            cart.recalculate_cart_total_price()
            self._update_cart(cart)
            return self.fetch_user_cart(logged_in_user)
        return cart

    @transaction.atomic
    def clear_cart(self, logged_in_user: User) -> Cart:
        cart: Cart = self.fetch_user_cart(logged_in_user)
        cart_repo.delete_cart_items(cart)
        cart.cart_items.clear()
        cart.recalculate_cart_total_price()
        self._update_cart(cart)
        return cart

    @transaction.atomic
    def add_order_to_cart(self, logged_in_user: User, order_uuid: str) -> None:
        self.clear_cart(logged_in_user)
        order = order_repo.find_order_by_uuid_with_products(order_uuid)
        cart: Cart = self.fetch_user_cart(logged_in_user)
        items = []
        for order_item in order.order_items.all():
            product_id = order_item.product.id
            quantity = order_item.quantity
            price = order_item.price
            cart_item = cart_repo.initialize_cart_item(quantity, price, quantity * price, product_id, cart)
            items.append(cart_item)
        cart.cart_items.add(*items, bulk=False)
        cart.recalculate_cart_total_price()
        self._update_cart(cart)

    @transaction.atomic
    def add_order_item_to_cart(self, logged_in_user: User, order_item_uuid: str) -> None:
        order_item = order_repo.find_order_item_by_uuid(order_item_uuid)
        cart: Cart = self.fetch_user_cart(logged_in_user)
        product_id = order_item.product.id
        quantity = order_item.quantity
        price = order_item.price
        existing_cart_item = next(filter(lambda ci: ci.product_id == product_id, cart.cart_items.all()), None)
        if existing_cart_item is None:
            cart_item = cart_repo.initialize_cart_item(quantity, price, quantity * price, product_id, cart)
            cart.cart_items.add(cart_item)
        else:
            new_quantity = existing_cart_item.quantity + quantity
            existing_cart_item.quantity = new_quantity
            existing_cart_item.total_price = new_quantity * price
            cart.cart_items.add(existing_cart_item)
        cart.recalculate_cart_total_price()
        self._update_cart(cart)

    def _update_cart(self, cart: Cart) -> Cart:
        return cart_repo.update_cart(cart)
