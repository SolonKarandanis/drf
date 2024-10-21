from dataclasses import dataclass


@dataclass
class CategoriesWithTotals:
    name: str
    total_products: int


@dataclass
class BrandsWithTotals:
    name: str
    total_products: int


@dataclass
class SizesWithTotals:
    name: str
    total_products: int


@dataclass
class DiscountsWithTotals:
    name: str
    total_products: int
