from rest_framework import serializers
from cfehome.serializers import ModelPaginationSerializer
from images.serializers import ImagesSerializer

from .models import CartItem, Cart
from .validators import is_quantity_valid
import json


class CartItemProductSerializer(serializers.Serializer):
    sku = serializers.CharField(read_only=True)
    title = serializers.CharField(read_only=True)
    uuid = serializers.CharField(read_only=True)

class CartItemSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='cart_item.id', read_only=True)
    modificationAlert = serializers.BooleanField(source='cart_item.modification_alert', read_only=True)
    unitPrice = serializers.FloatField(source='cart_item.unit_price', read_only=True)
    quantity = serializers.IntegerField(source='cart_item.quantity', read_only=True)
    totalPrice = serializers.FloatField(source='cart_item.total_price', read_only=True)
    productId = serializers.IntegerField(source='cart_item.product_id', read_only=True)
    uuid = serializers.CharField(source='cart_item.uuid', read_only=True)
    attributes = serializers.SerializerMethodField('_get_attributes_as_json')
    previewImage = ImagesSerializer(source='preview_image', read_only=True)
    productDetails = CartItemProductSerializer(source='product_details', read_only=True)

    def _get_attributes_as_json(self, obj):
        cart_item = getattr(obj, 'cart_item')
        attributes = getattr(cart_item, 'attributes')
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
            'productDetails',
            'attributes',
            'previewImage'
        ]


class PaginatedCartItemListSerializer(ModelPaginationSerializer):
    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = CartItemSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}


class CartSerializer(serializers.Serializer):
    id = serializers.IntegerField(source='cart.id', read_only=True)
    modificationAlert = serializers.BooleanField(source='cart.modification_alert', read_only=True)
    totalPrice = serializers.FloatField(source='cart.total_price', read_only=True)
    dateCreated = serializers.DateTimeField(source='cart.date_created', read_only=True)
    dateModified = serializers.DateTimeField(source='cart.date_modified', read_only=True)
    uuid = serializers.CharField(source='cart.uuid', read_only=True)
    cartItems = CartItemSerializer(source='cart_items', many=True, read_only=True)

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
