from dataclasses import dataclass
from typing import List

from images.models import Images
from products.models import Product, ProductAttributeValues


@dataclass
class CategoriesWithTotals:
    id: int
    name: str
    total_products: int


@dataclass
class BrandsWithTotals:
    id: int
    name: str
    total_products: int


@dataclass
class SizesWithTotals:
    id: int
    name: str
    total_products: int


@dataclass
class DiscountsWithTotals:
    id: int
    name: str
    total_products: int


@dataclass
class ProductWithPreviewImage:
    product: Product
    preview_image: Images


@dataclass
class ProductAttributes:
    colors: List[ProductAttributeValues]
    sizes: List[ProductAttributeValues]
    genders: List[ProductAttributeValues]
