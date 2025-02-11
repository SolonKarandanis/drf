from dataclasses import dataclass
from typing import List

from cart.models import CartItem, Cart
from images.models import Images


@dataclass
class CartItemWithPreviewImage:
    cart_item: CartItem
    preview_image: Images


@dataclass
class CartDto:
    cart: Cart
    cart_items: List[CartItemWithPreviewImage]
