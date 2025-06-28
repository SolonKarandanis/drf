from typing import List

from django.conf import settings
import logging

from django.db import transaction

from images.image_service import ImageService
from products.models import Product
from products.product_service import ProductService
from wishlist.dtos import WishlistItemWithPreviewImage, WishlistItemProduct
from wishlist.models import WishListItem
from wishlist.wishlist_repository import WishListRepository

wishlist_repo = WishListRepository()
product_service = ProductService()
image_service = ImageService()

User = settings.AUTH_USER_MODEL

logger = logging.getLogger('django')


class WishlistService:

    @transaction.atomic
    def fetch_user_wish_list_items_dto(self, logged_in_user: User) -> List[WishlistItemWithPreviewImage]:
        wishlist_items = self.fetch_user_wish_list_items(logged_in_user)
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

    def delete_wish_list_items(self, request, logged_in_user: User) -> None:
        items = self.fetch_user_wish_list_items(logged_in_user)
