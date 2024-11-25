import logging

from django.conf import settings
from typing import List
from django.db.models import Count

from .dtos import CategoriesWithTotals, BrandsWithTotals, SizesWithTotals
from .models import Product, Category, Brand, AttributeOptions, ProductAttributeValues

User = settings.AUTH_USER_MODEL
logger = logging.getLogger('django')


class ProductRepository:

    def find_by_uuid(self, uuid: str, fetch_children: bool = True) -> Product:
        qs = Product.objects.get_queryset()
        if fetch_children:
            return qs.with_brand().with_comments().with_categories().by_uuid(uuid)
        return qs.by_uuid(uuid)

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

    def search_products(self, query: str, categories: List[int],
                        brands: List[int], sizes: List[int], user: User) -> List[Product]:
        return Product.objects.get_queryset().fts_search(query, categories, brands, sizes, user)

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

    def get_brands_with_totals(self) -> List[BrandsWithTotals]:
        brands_with_totals_qs = Brand.objects \
            .annotate(products_count=Count('product')) \
            .filter(products_count__gt=0) \
            .order_by('-products_count')
        result_list: List[BrandsWithTotals] = [
            BrandsWithTotals(id=brand.id, name=brand.name, total_products=brand.products_count)
            for brand in brands_with_totals_qs
        ]
        return result_list

    def get_discounts_with_totals(self):
        pass

    def get_sizes_with_totals(self) -> List[SizesWithTotals]:
        sizes_with_totals_qs = ProductAttributeValues.objects \
            .raw("SELECT 1 id, pav.attribute_option_id ,pao.option_name, COUNT(pav.product_id) as total_products "
                 "FROM products_attribute_values pav "
                 "JOIN products_attribute_options pao ON pao.id =pav.attribute_option_id "
                 "WHERE pav.attribute_id =1 "
                 "GROUP BY pav.attribute_option_id ,pao.option_name "
                 "HAVING COUNT(pav.product_id) > 0")
        result_list: List[SizesWithTotals] = [
            SizesWithTotals(id=sizes.attribute_option_id, name=sizes.option_name,  total_products=sizes.total_products)
            for sizes in sizes_with_totals_qs
        ]
        return result_list
