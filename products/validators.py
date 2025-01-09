from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .product_repository import ProductRepository

repo = ProductRepository()


def validate_sku(self):
    exists = repo.exists_product_by_sku(self)
    if exists:
        raise serializers.ValidationError(f"{self} is already a product sku")
    return self


def product_exists(self):
    exists = repo.exists_product_by_id(self)
    if not exists:
        raise serializers.ValidationError(f"Product does not exist")
    return self


unique_product_title = UniqueValidator(queryset=repo.find_all_products(), lookup='iexact')
