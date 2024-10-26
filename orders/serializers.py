import logging

from rest_framework import serializers
from .models import Order, OrderItem
from cfehome.serializers import ModelPaginationSerializer
from comments.serializers import CommentSerializer

from .validators import order_exists

logger = logging.getLogger('django')


class OrderItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(source='product_id', read_only=True)
    productName = serializers.CharField(source='product_name', read_only=True)
    startDate = serializers.DateField(source='start_date', read_only=True)
    endDate = serializers.DateField(source='end_date', read_only=True)
    totalPrice = serializers.IntegerField(source='total_price', read_only=True)


    class Meta:
        model = OrderItem
        fields = [
            'id',
            'productId',
            'productName',
            'sku',
            'manufacturer',
            'startDate',
            'endDate',
            'status',
            'price',
            'quantity',
            'totalPrice',
            'uuid',
        ]


class OrderSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    buyerId = serializers.IntegerField(source='buyer_id', read_only=True)
    supplierId = serializers.IntegerField(source='supplier_id', read_only=True)
    productName = serializers.CharField(source='product_name', read_only=True)
    dateShipped = serializers.DateField(source='date_shipped', read_only=True)
    isShipped = serializers.BooleanField(source='is_shipped', read_only=True)
    totalPrice = serializers.IntegerField(source='total_price', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'date_created',
            'buyerId',
            'supplierId',
            'status',
            'totalPrice',
            'isShipped',
            'dateShipped',
            'uuid',
            'orderItems',
            'comments'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    dateCreated = serializers.DateField(source='date_created', read_only=True)
    buyerId = serializers.IntegerField(source='buyer_id', read_only=True)
    supplierId = serializers.IntegerField(source='supplier_id', read_only=True)
    totalPrice = serializers.IntegerField(source='total_price', read_only=True)
    isShipped = serializers.BooleanField(source='is_shipped', read_only=True)
    dateShipped = serializers.DateField(source='date_shipped', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'dateCreated',
            'buyerId',
            'supplierId',
            'status',
            'totalPrice',
            'isShipped',
            'dateShipped',
            'uuid'
        ]


class PaginatedOrderSerializer(ModelPaginationSerializer):
    """
    Serializes page objects of order querysets.
    """

    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = OrderListSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}


class PostOrderComment(serializers.Serializer):
    order_id = serializers.IntegerField(validators=[order_exists])
    comment = serializers.CharField()

    def __repr__(self):
        return f"<PostOrderComment OrderId:{self.order_id},  Comment:{self.comment}>"


class SearchOrderItems(serializers.Serializer):
    query = serializers.CharField()

    def __repr__(self):
        return f"<SearchOrderItems query:{self.query}>"
