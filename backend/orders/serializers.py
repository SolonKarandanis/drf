import logging

from rest_framework import serializers
from .models import Order, OrderItem
from cfehome.serializers import ModelPaginationSerializer

logger = logging.getLogger('django')


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id',
        ]


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id',
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