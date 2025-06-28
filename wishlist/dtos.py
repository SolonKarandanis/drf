from dataclasses import dataclass

from images.models import Images
from wishlist.models import WishListItem


@dataclass
class WishlistItemProduct:
    sku: str
    title: str
    uuid: str


@dataclass
class WishlistItemWithPreviewImage:
    wishlist_item: WishListItem
    preview_image: Images
    product_details: WishlistItemProduct
