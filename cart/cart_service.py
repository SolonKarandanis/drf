from typing import List
import json

from django.conf import settings
from django.db import transaction
from rest_framework import serializers
from images.image_service import ImageService
from products.constants import SIZE_ATTRIBUTE_OPTION_ID, COLOR_ATTRIBUTE_OPTION_ID
from products.product_service import ProductService
from .dtos import CartDto, CartItemWithPreviewImage, CartItemProduct
from .models import Cart, CartItem
from products.models import Product
from .cart_repository import CartRepository
from orders.order_repository import OrderRepository

import logging

from .serializers import AddToCart, UpdateItem, DeleteCartItems

cart_repo = CartRepository()
order_repo = OrderRepository()
product_service = ProductService()
image_service = ImageService()

User = settings.AUTH_USER_MODEL
key_prefix = settings.CACHES.get('default').get('KEY_PREFIX')

logger = logging.getLogger('django')


class CartService:

    @transaction.atomic
    def fetch_user_cart_dto(self, logged_in_user: User) -> CartDto:
        cart = self._fetch_user_cart(logged_in_user)
        cart_items: List[CartItem] = cart.cart_items.all()
        product_ids = [cart_item.product_id for cart_item in cart_items]
        product_preview_images = image_service.find_product_profile_images(product_ids)
        products = product_service.find_products_by_ids(product_ids)

        product_dict: dict[int, Product] = {product.id: product for product in products}
        product_preview_images_dict = {image.object_id: image for image in product_preview_images}

        cart_items_with_preview_images = []
        for cart_item in cart_items:
            product_id = cart_item.product_id
            product = product_dict.get(product_id)
            product_attributes = product_service.find_product_attributes(product.uuid)
            cart_item_product = CartItemProduct(sku=product.sku, title=product.title, uuid=product.uuid)
            cart_item_with_preview_image = CartItemWithPreviewImage(
                cart_item=cart_item,
                preview_image=product_preview_images_dict.get(product_id),
                product_details=cart_item_product,
                product_attributes=product_attributes
            )
            cart_items_with_preview_images.append(cart_item_with_preview_image)

        cart_dto = CartDto(cart=cart, cart_items=cart_items_with_preview_images)
        return cart_dto

    def _fetch_user_cart(self, logged_in_user: User) -> Cart:
        cart = cart_repo.fetch_user_cart(logged_in_user)
        logger.info(f'cart: {cart}')
        return cart

    def fetch_user_cart_with_products_and_users(self, logged_in_user: User) -> Cart:
        return cart_repo.fetch_user_cart_with_products_and_users(logged_in_user)

    @transaction.atomic
    def add_to_cart(self, request: AddToCart, logged_in_user: User) -> None:
        cart: Cart = self._fetch_user_cart(logged_in_user)
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        product_ids = [d['productId'] for d in data_list]
        products_to_be_added: List[Product] = product_service.find_products_by_ids(product_ids)
        product_quantities_dict = {d['productId']: d['quantity'] for d in data_list}
        product_attributes_dict = {d['productId']: d['attributes'] if "attributes" in d else None for d in data_list}
        items = []
        for product in products_to_be_added:
            product_id = product.id
            quantity = product_quantities_dict[product_id]
            price = product.price
            product_attributes = product_attributes_dict[product_id]
            if product_attributes is None:
                size_product_attribute = product_service.find_first_product_attribute_value_size_by_product_id(
                    product_id)
                color_product_attribute = product_service.find_first_product_attribute_value_color_by_product_id(
                    product_id)
                default_attributes = {SIZE_ATTRIBUTE_OPTION_ID: size_product_attribute.attribute_option_id,
                                      COLOR_ATTRIBUTE_OPTION_ID: color_product_attribute.attribute_option_id}
                product_attributes = json.dumps(default_attributes)
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
        cart.recalculate_cart_total_price()
        self._update_cart(cart)

    def _find_existing_cart_item(self, product_id: int, cart_items: List[CartItem],
                                 product_attributes: str) -> CartItem | None:
        if len(cart_items) == 0:
            return None
        for cart_item in cart_items:
            if cart_item.attributes == product_attributes and cart_item.product_id == product_id:
                return cart_item
        return None

    @transaction.atomic
    def update_items(self, request: UpdateItem, logged_in_user: User) -> None:
        cart: Cart = self._fetch_user_cart(logged_in_user)
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        for data in data_list:
            attributes = None
            quantity = data['quantity']
            cart_item_id = data['cartItemId']
            product_id = data['productId']
            if "attributes" in data:
                attributes = data['attributes']
            existing_cart_item = self._find_existing_cart_item_for_update(cart_item_id, product_id,
                                                                          cart.cart_items.all(), attributes)
            logger.info(
                f'---> CartService ---> update_items ---> existing_cart_item: {existing_cart_item}')
        #     if existing_cart_item is not None:
        #         existing_cart_item.quantity = quantity
        #         existing_cart_item.total_price = quantity * existing_cart_item.unit_price
        #         if attributes is not None:
        #             existing_cart_item.attributes = attributes
        #         cart_repo.update_cart_item(existing_cart_item)
        # cart = self._fetch_user_cart(logged_in_user)
        # cart.recalculate_cart_total_price()
        # self._update_cart(cart)

    def _find_existing_cart_item_for_update(self, cart_item_id: int,  product_id: int, cart_items: List[CartItem],
                                            attributes: str) -> CartItem | None:
        if len(cart_items) == 0:
            return None
        for cart_item in cart_items:
            if cart_item.id == cart_item_id:
                logger.info(
                    f'---> CartService ---> update_items ---> cart_item.id == cart_item_id')
                return cart_item
            if attributes is not None and cart_item.id != cart_item_id and cart_item.product_id == product_id \
                    and cart_item.attributes == attributes:
                logger.info(
                    f'---> CartService ---> update_items ---> cart_item.id != cart_item_id')
                raise serializers.ValidationError({'attributes': "Cart Item already exists with these attributes"})
        return None

    @transaction.atomic
    def delete_cart_items(self, request: DeleteCartItems, logged_in_user: User) -> None:
        cart: Cart = self._fetch_user_cart(logged_in_user)
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        cart_item_ids = [d['cartItemId'] for d in data_list]
        existing_cart_items = list(filter(lambda ci: ci.id in cart_item_ids, cart.cart_items.all()))
        logger.info(f'items: {existing_cart_items}')
        if existing_cart_items is not None:
            cart.cart_items.remove(*existing_cart_items)
            cart.recalculate_cart_total_price()
            self._update_cart(cart)

    @transaction.atomic
    def clear_cart(self, logged_in_user: User) -> None:
        cart: Cart = self._fetch_user_cart(logged_in_user)
        cart_repo.delete_cart_items(cart)
        cart.cart_items.clear()
        cart.recalculate_cart_total_price()
        self._update_cart(cart)

    @transaction.atomic
    def add_order_to_cart(self, logged_in_user: User, order_uuid: str) -> None:
        self.clear_cart(logged_in_user)
        order = order_repo.find_order_by_uuid_with_products(order_uuid)
        cart: Cart = self._fetch_user_cart(logged_in_user)
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
        cart: Cart = self._fetch_user_cart(logged_in_user)
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
