import logging

from django.shortcuts import get_object_or_404
from django.conf import settings
from typing import List
from django.db.models import Count

from cfehome.repository import IRepository
from .dtos import CategoriesWithTotals
from .models import Product, Category

User = settings.AUTH_USER_MODEL
logger = logging.getLogger('django')


class ProductRepository:

    def find_by_uuid(self, uuid: str) -> Product:
        product = Product.objects.get_queryset().with_comments().by_uuid(uuid)
        return product

    def find_by_id(self, product_id: int) -> Product:
        product = Product.objects.get_queryset().with_comments().get(pk=product_id)
        return product

    def find_users_product_by_id(self, product_id: int, logged_in_user: User) -> Product:
        product = Product.objects.get_queryset().owned_by(logged_in_user) \
            .with_comments().get(pk=product_id)
        return product

    def find_users_product_by_uuid(self, uuid: str, logged_in_user: User) -> Product:
        product = Product.objects.get_queryset().owned_by(logged_in_user) \
            .with_comments().by_uuid(uuid)
        return product

    def find_all_products(self) -> List[Product]:
        products = Product.objects.all()
        return products

    def find_supplier_products(self, logged_in_user: User) -> List[Product]:
        products = Product.objects.get_queryset().owned_by(logged_in_user)
        return products

    def find_products_by_ids(self, product_ids: List[int]) -> List[Product]:
        products = Product.objects.filter(pk__in=product_ids)
        return products

    def update_product_price(self, product: Product) -> Product:
        product.save(update_fields=['price'])
        return product

    def find_public_products(self) -> List[Product]:
        products = Product.objects.get_queryset().is_public()
        return products

    def find_product_skus(self) -> List[str]:
        return Product.objects.get_queryset().product_skus()

    def search_products(self, query: str, user: User) -> List[Product]:
        return Product.objects.get_queryset().fts_search(query, user)

    def get_categories_with_totals(self) -> List[CategoriesWithTotals]:
        categories_with_totals_qs = Category.objects \
            .annotate(products_count=Count('product')) \
            .filter(products_count__gt=0) \
            .order_by('-products_count')
        result_list: List[CategoriesWithTotals] = [
            CategoriesWithTotals(id=category.id, name=category.name, total_products=category.products_count)
            for category in categories_with_totals_qs
        ]
        return result_list

    def get_brands_with_totals(self):
        brands_with_totals_qs = Product.objects \
            .annotate(brands_count=Count('brand')) \
            .order_by('-brands_count')
        logger.info(f'brands_with_totals_qs: {brands_with_totals_qs}')
        return brands_with_totals_qs

    def get_discounts_with_totals(self):
        pass

    def get_sizes_with_totals(self):
        sizes_with_totals_qs = Product.objects \
            .filter(attributes=1) \
            .annotate(sizes_count=Count('attributes')) \
            .order_by('-sizes_count')
        logger.info(f'sizes_with_totals_qs: {sizes_with_totals_qs}')
        return sizes_with_totals_qs
