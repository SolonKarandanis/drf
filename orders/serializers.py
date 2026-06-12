import logging

from rest_framework import serializers
from .models import Order, OrderItem
from cfehome.serializers import ModelPaginationSerializer
from comments.serializers import CommentSerializer
from auth.serializers import UserPublicSerializer

from .validators import order_exists

logger = logging.getLogger('django')


class OrderItemSerializer(serializers.ModelSerializer):
    productId = serializers.IntegerField(source='product_id', read_only=True)
    productName = serializers.CharField(source='product_name', read_only=True)
    startDate = serializers.DateTimeField(source='start_date', read_only=True)
    endDate = serializers.DateTimeField(source='end_date', read_only=True)
    totalPrice = serializers.FloatField(source='total_price', read_only=True)

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
    orderItems = OrderItemSerializer(many=True, read_only=True, source='order_items')
    comments = CommentSerializer(many=True, read_only=True)
    buyer = UserPublicSerializer(read_only=True)
    supplier = UserPublicSerializer(read_only=True)
    dateCreated = serializers.DateTimeField(source='date_created', read_only=True)
    dateShipped = serializers.DateTimeField(source='date_shipped', read_only=True)
    isShipped = serializers.BooleanField(source='is_shipped', read_only=True)
    totalPrice = serializers.FloatField(source='total_price', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'dateCreated',
            'buyer',
            'supplier',
            'status',
            'totalPrice',
            'isShipped',
            'dateShipped',
            'uuid',
            'orderItems',
            'comments'
        ]


class OrderListSerializer(serializers.ModelSerializer):
    dateCreated = serializers.DateTimeField(source='date_created', read_only=True)
    buyer = UserPublicSerializer(read_only=True)
    supplier = UserPublicSerializer(read_only=True)
    totalPrice = serializers.FloatField(source='total_price', read_only=True)
    isShipped = serializers.BooleanField(source='is_shipped', read_only=True)
    dateShipped = serializers.DateTimeField(source='date_shipped', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'dateCreated',
            'buyer',
            'supplier',
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
