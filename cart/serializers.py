from rest_framework import serializers
from cfehome.serializers import ModelPaginationSerializer

from .models import CartItem, Cart
from .validators import is_quantity_valid


class CartItemSerializer(serializers.ModelSerializer):
    modificationAlert = serializers.BooleanField(source='modification_alert', read_only=True)
    unitPrice = serializers.IntegerField(source='unit_price', read_only=True)
    totalPrice = serializers.IntegerField(source='total_price', read_only=True)
    productId = serializers.IntegerField(source='product_id', read_only=True)

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
        ]


class PaginatedCartItemListSerializer(ModelPaginationSerializer):
    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = CartItemSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}


class CartSerializer(serializers.ModelSerializer):
    cartItems = CartItemSerializer(many=True, read_only=True)
    modificationAlert = serializers.BooleanField(source='modification_alert', read_only=True)
    totalPrice = serializers.IntegerField(source='total_price', read_only=True)
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
    attributes = serializers.SerializerMethodField(required=False)

    class Meta:
        fields = [
            'productId',
            'quantity',
            'attributes',
        ]

    def get_attributes(self, obj):
        if "attributes" not in obj:
            return None
        return obj.attributes

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
