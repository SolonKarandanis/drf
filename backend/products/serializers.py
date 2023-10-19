from rest_framework import serializers

from .models import Product
from .validators import unique_product_title
from auth.serializers import UserPublicSerializer


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[unique_product_title])
    owner = UserPublicSerializer(source='user', read_only=True)
    class Meta:
        model = Product
        fields = [
            'owner',
            'id',
            'title',
            'content',
            'price',
            'sale_price'
        ]
