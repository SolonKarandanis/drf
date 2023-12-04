from django.shortcuts import get_object_or_404
from django.conf import settings
from typing import List

from cfehome.repository import IRepository
from .models import Product

User = settings.AUTH_USER_MODEL


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
