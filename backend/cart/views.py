from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import logging

# Create your views here.
from .models import Cart
from products.models import Product
from .serializers import CartSerializer, AddToCart, UpdateQuantity, DeleteCartItems

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    logged_in_user = request.user
    cart = Cart.objects.get_queryset() \
        .with_cart_items() \
        .owned_by(logged_in_user)
    logger.info(f'cart: {cart}')
    data = CartSerializer(cart).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_cart_items(request):
    logged_in_user = request.user
    cart = Cart.objects.get_queryset() \
        .with_cart_items() \
        .owned_by(logged_in_user)
    logger.info(f'cart: {cart}')
    serializer = AddToCart(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        data_list = [dict(item) for item in data]
        product_ids = [d['product_id'] for d in data_list]
        products_to_be_added = Product.objects.filter(pk__in=product_ids)
        product_quantities_dict = {d['product_id']: d['quantity'] for d in data_list}
        cart.add_items_to_cart(product_quantities_dict, products_to_be_added)
        data = CartSerializer(cart).data
        return Response(data, status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quantities(request, pk):
    logged_in_user = request.user
    cart = Cart.objects.get_queryset() \
        .with_cart_items() \
        .owned_by(logged_in_user)
    logger.info(f'cart: {cart}')
    serializer = UpdateQuantity(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        quantity = data['quantity']
        cart.update_item_quantity(pk, quantity)
        data = CartSerializer(cart).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_items(request):
    logged_in_user = request.user
    cart = Cart.objects.get_queryset() \
        .with_cart_items() \
        .owned_by(logged_in_user)
    logger.info(f'cart: {cart}')
    serializer = DeleteCartItems(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        data = serializer.data
        data_list = [dict(item) for item in data]
        cart_item_ids = [d['cart_item_id'] for d in data_list]
        cart.remove_from_cart(cart_item_ids)
        data = CartSerializer(cart).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    logged_in_user = request.user
    cart = Cart.objects.get_queryset() \
        .with_cart_items() \
        .owned_by(logged_in_user)
    logger.info(f'cart: {cart}')
    cart.clear_cart()
    data = CartSerializer(cart).data
    return Response(data, status=status.HTTP_200_OK)
