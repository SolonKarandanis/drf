from dataclasses import dataclass


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
