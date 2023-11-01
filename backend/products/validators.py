from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product


def validate_sku(self):
    qs = Product.objects.filter(sku=self)
    if qs.exists():
        raise serializers.ValidationError(f"{self} is already a product sku")
    return self


unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')
