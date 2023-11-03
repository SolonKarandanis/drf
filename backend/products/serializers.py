import logging

from rest_framework import serializers
from .models import Product
from .validators import unique_product_title, validate_sku
from auth.serializers import UserPublicSerializer
from cfehome.serializers import ModelPaginationSerializer

logger = logging.getLogger('django')


class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(validators=[unique_product_title])
    owner = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'owner',
            'price',
            'inventory',
            'sale_price'
        ]


class ProductListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'price',
            'inventory',
            'sale_price'
        ]


class PaginatedProductListSerializer(ModelPaginationSerializer):
    """
    Serializes page objects of product querysets.
    """

    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = ProductListSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}


class CreateProductSerializer(serializers.ModelSerializer):
    sku = serializers.CharField(validators=[validate_sku])
    title = serializers.CharField(validators=[unique_product_title])
    owner = UserPublicSerializer(source='user', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'sku',
            'title',
            'content',
            'owner',
            'price',
            'inventory',
        ]

    def save(self):
        user = self.context.get("logged_in_user")
        sku = self.validated_data['sku']
        title = self.validated_data['title']
        content = self.validated_data['content']
        price = self.validated_data['price']
        inventory = self.validated_data['inventory']
        new_product = Product(sku=sku, user=user, title=title, content=content, price=price, inventory=inventory)
        new_product.save()
        return new_product
