from rest_framework import serializers
from cfehome.serializers import ModelPaginationSerializer

from .models import CartItem, Cart
from .validators import is_quantity_valid


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = [
            'id',
            'modification_alert',
            'quantity',
            'unit_price',
            'total_price',
            'product_id'
        ]


class PaginatedCartItemListSerializer(ModelPaginationSerializer):
    def __init__(self, data, request):
        super().__init__(data, request)
        serializer = CartItemSerializer(data, many=True)
        self.data = {'count': self.page_data.get('count'), 'previous': self.page_data.get('previous'),
                     'next': self.page_data.get('next'), 'data': serializer.data}


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            'id',
            'modification_alert',
            'total_price',
            'date_created',
            'date_modified',
            'cart_items',
        ]


class AddToCart(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(validators=[is_quantity_valid])

    def __repr__(self):
        return f"<AddOrUpdateCart ProductId:{self.product_id},  Quantity:{self.quantity}>"


class UpdateQuantity(serializers.Serializer):
    cart_item_id = serializers.IntegerField()
    quantity = serializers.IntegerField(validators=[is_quantity_valid])


    def __repr__(self):
        return f"<UpdateQuantity CartItemId:{self.cart_item_id},  Quantity:{self.quantity}>"


class DeleteCartItems(serializers.Serializer):
    cart_item_id = serializers.IntegerField()
