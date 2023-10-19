from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Product


def validate_title(self, value):
    qs = Product.objects.filter(title=value)
    if qs.exists():
        raise serializers.ValidationError(f"{value} is already a product name")
    return value


unique_product_title = UniqueValidator(queryset=Product.objects.all(), lookup='iexact')
