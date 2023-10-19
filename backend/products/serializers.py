from rest_framework import serializers

from .models import Product
from .validators import unique_product_title


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[unique_product_title])
    class Meta:
        model = Product
        fields = [
            'id',
            'title',
            'content',
            'price',
            'sale_price'
        ]

    def validate_title(self, value):
        qs = Product.objects.filter(title=value)
        if qs.exists():
            raise serializers.ValidationError(f"{value} is already a product name")
        return value