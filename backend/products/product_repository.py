from django.shortcuts import get_object_or_404
from django.conf import settings

from cfehome.repository import IRepository
from .models import Product

User = settings.AUTH_USER_MODEL


class ProductRepository():

    def find_by_id(self, product_id: int) -> Product:
        product = get_object_or_404(Product, pk=product_id)
        return product

    def find_users_product_by_id(self, product_id: int, logged_in_user: User) -> Product:
        product = Product.objects.get_queryset().owned_by(logged_in_user).get(pk=product_id)
        return product

    def find_all_products(self):
        products = Product.objects.all()
        return products

    def find_supplier_products(self, logged_in_user: User):
        products = Product.objects.get_queryset().owned_by(logged_in_user)
        return products
