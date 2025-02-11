from rest_framework import serializers
from cfehome.serializers import ModelPaginationSerializer
from images.serializers import ImagesSerializer

from .models import CartItem, Cart
from .validators import is_quantity_valid
import json


class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='cart_item.id', read_only=True)
    modificationAlert = serializers.BooleanField(source='cart_item.modification_alert', read_only=True)
    unitPrice = serializers.IntegerField(source='cart_item.unit_price', read_only=True)
    totalPrice = serializers.IntegerField(source='cart_item.total_price', read_only=True)
    productId = serializers.IntegerField(source='cart_item.product_id', read_only=True)
    uuid = serializers.CharField(source='cart_item.uuid', read_only=True)
    attributes = serializers.SerializerMethodField('_get_attributes_as_json')
    previewImage = ImagesSerializer(source='preview_image', read_only=True)

    def _get_attributes_as_json(self, cart_item):
        attributes = getattr(cart_item, 'cart_item.attributes')
        return json.loads(attributes)

    class Meta:
        model = CartItem
        fields = [
            'id',
            'modificationAlert',
            'quantity',
            'unitPrice',
            'totalPrice',
            'uuid',
            'productId',
            'attributes',
            'previewImage'
        ]


class PaginatedCartItemListSerializer(ModelPaginationSerializer):
    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = CartItemSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}


class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(source='cart_items', many=True, read_only=True)
    modificationAlert = serializers.BooleanField(source='modification_alert', read_only=True)
    totalPrice = serializers.FloatField(source='total_price', read_only=True)
    dateCreated = serializers.DateTimeField(source='date_created', read_only=True)
    dateModified = serializers.DateTimeField(source='date_modified', read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'modificationAlert',
            'totalPrice',
            'dateCreated',
            'dateModified',
            'uuid',
            'cartItems',
        ]


class AddToCart(serializers.Serializer):
    productId = serializers.IntegerField()
    quantity = serializers.IntegerField(validators=[is_quantity_valid])
    attributes = serializers.CharField(required=False)

    class Meta:
        fields = [
            'productId',
            'quantity',
            'attributes',
        ]

    def __repr__(self):
        return f"<AddOrUpdateCart ProductId:{self.product_id},  Quantity:{self.quantity}>"


class UpdateQuantity(serializers.Serializer):
    cartItemId = serializers.IntegerField(source='cart_item_id', read_only=True)
    quantity = serializers.IntegerField(validators=[is_quantity_valid])

    class Meta:
        fields = [
            'cartItemId',
            'quantity',
        ]

    def __repr__(self):
        return f"<UpdateQuantity CartItemId:{self.cart_item_id},  Quantity:{self.quantity}>"


class DeleteCartItems(serializers.Serializer):
    cartItemId = serializers.IntegerField(source='cart_item_id', read_only=True)

    class Meta:
        fields = [
            'cartItemId'
        ]
