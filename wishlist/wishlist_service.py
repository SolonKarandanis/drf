import json
from typing import List

from django.conf import settings
import logging

from django.db import transaction

from images.image_service import ImageService
from products.constants import SIZE_ATTRIBUTE_OPTION_ID, COLOR_ATTRIBUTE_OPTION_ID
from products.models import Product
from products.product_service import ProductService
from wishlist.dtos import WishlistItemWithPreviewImage, WishlistItemProduct
from wishlist.models import WishListItem
from wishlist.serializers import AddToWishList, RemoveWishListItem
from wishlist.wishlist_repository import WishListRepository

wishlist_repo = WishListRepository()
product_service = ProductService()
image_service = ImageService()

User = settings.AUTH_USER_MODEL

logger = logging.getLogger('django')


class WishlistService:

    @transaction.atomic
    def fetch_user_wish_list_items_dto(self,  logged_in_user: User, query: str = '') \
            -> List[WishlistItemWithPreviewImage]:
        wishlist_items = self.fetch_user_wish_list_items_with_product(logged_in_user)
        product_ids = [wishlist_item.product_id for wishlist_item in wishlist_items]
        product_preview_images = image_service.find_product_profile_images(product_ids)
        products = product_service.find_products_by_ids(product_ids)
        product_dict: dict[int, Product] = {product.id: product for product in products}
        product_preview_images_dict = {image.object_id: image for image in product_preview_images}

        wishlist_items_with_preview_images = []
        for wishlist_item in wishlist_items:
            product_id = wishlist_item.product_id
            product = product_dict.get(product_id)
            wishlist_item_product = WishlistItemProduct(sku=product.sku, title=product.title, uuid=product.uuid)
            wishlist_item_with_preview_image = WishlistItemWithPreviewImage(
                wishlist_item=wishlist_item,
                preview_image=product_preview_images_dict.get(product_id),
                product_details=wishlist_item_product,
            )
            wishlist_items_with_preview_images.append(wishlist_item_with_preview_image)
        return wishlist_items_with_preview_images

    def fetch_user_wish_list_items(self, logged_in_user: User) -> List[WishListItem]:
        return wishlist_repo.fetch_user_wish_list_items(logged_in_user)

    def fetch_user_wish_list_items_with_product(self, logged_in_user: User) -> List[WishListItem]:
        return wishlist_repo.fetch_user_wish_list_items_with_product(logged_in_user)

    @transaction.atomic
    def add_wishlist_item(self, request: AddToWishList, logged_in_user: User) -> None:
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        product_ids = [d['productId'] for d in data_list]
        product_attributes_dict = {d['productId']: d['attributes'] if "attributes" in d else None for d in data_list}
        products_to_be_added: List[Product] = product_service.find_products_by_ids(product_ids)
        items = []
        for product in products_to_be_added:
            product_id = product.id
            product_attributes = product_attributes_dict[product_id]
            if product_attributes is None:
                size_product_attribute = product_service.find_first_product_attribute_value_size_by_product_id(
                    product_id)
                color_product_attribute = product_service.find_first_product_attribute_value_color_by_product_id(
                    product_id)
                default_attributes = {SIZE_ATTRIBUTE_OPTION_ID: size_product_attribute.attribute_option_id,
                                      COLOR_ATTRIBUTE_OPTION_ID: color_product_attribute.attribute_option_id}
                product_attributes = json.dumps(default_attributes)
            wishlist_item_exists = wishlist_repo \
                .exists_by_user_and_product_and_attributes(product, logged_in_user, product_attributes)
            if not wishlist_item_exists:
                wishlist_item = wishlist_repo.initialize_wish_list_item(product=product, user=logged_in_user,
                                                                        attributes=product_attributes)
                items.append(wishlist_item)
        if len(items) >= 0:
            wishlist_repo.create_wishlist_items(items)

    @transaction.atomic
    def delete_wish_list_items(self, request: RemoveWishListItem, logged_in_user: User) -> None:
        items = self.fetch_user_wish_list_items(logged_in_user)
        serialized_data = request.data
        data_list = [dict(item) for item in serialized_data]
        wishlist_item_ids = [d['wishListItemId'] for d in data_list]
        existing_wishlist_items = list(filter(lambda ci: ci.id in wishlist_item_ids, items))
        existing_wishlist_item_ids = [item.id for item in existing_wishlist_items]
        if existing_wishlist_item_ids is not None:
            wishlist_repo.delete_wish_list_items_by_ids(existing_wishlist_item_ids)
