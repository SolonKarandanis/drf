from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.core.cache import cache
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
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = fetch_user_cart(logged_in_user)
    data = CartSerializer(cart).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_cart_items(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = fetch_user_cart(logged_in_user)
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
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = fetch_user_cart(logged_in_user)
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
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = fetch_user_cart(logged_in_user)
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
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = fetch_user_cart(logged_in_user)
    cart.clear_cart()
    data = CartSerializer(cart).data
    return Response(data, status=status.HTTP_200_OK)


def fetch_user_cart(logged_in_user):
    user_id = logged_in_user.id
    cache_key = f'cart-{user_id}'
    cart = cache.get('cart')
    if cart is None:
        cart = Cart.objects.get_queryset() \
            .with_cart_items() \
            .owned_by(logged_in_user)
        cache.set(cache_key, cart, timeout=120)
    logger.info(f'cart: {cart}')
    return cart