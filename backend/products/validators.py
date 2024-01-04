from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product


def validate_sku(self):
    qs = Product.objects.filter(sku=self)
    if qs.exists():
        raise serializers.ValidationError(f"{self} is already a product sku")
    return self


def product_exists(self):
    qs = Product.objects.filter(pk=self)
    exists = qs.exists()
    if not exists:
        raise serializers.ValidationError(f"Product does not exist")
    return self


unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')
