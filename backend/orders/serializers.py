import logging

from rest_framework import serializers
from .models import Order, OrderItem
from cfehome.serializers import ModelPaginationSerializer

logger = logging.getLogger('django')


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
            'product_name',
            'sku',
            'manufacturer',
            'start_date',
            'end_date',
            'status',
            'price',
            'quantity',
            'total_price',
            'uuid',
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'date_created',
            'status',
            'total_price',
            'is_shipped',
            'date_shipped',
            'uuid',
            'order_items'
        ]


class PaginatedOrderSerializer(ModelPaginationSerializer):
    """
    Serializes page objects of order querysets.
    """

    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = OrderSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}
