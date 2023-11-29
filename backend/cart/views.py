from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import logging

# Create your views here.
from .serializers import CartSerializer, AddToCart, UpdateQuantity, DeleteCartItems
from .cart_service import CartService
cart_service = CartService()

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = cart_service.fetch_user_cart(logged_in_user)
    data = CartSerializer(cart).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_cart_items(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    serializer = AddToCart(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        cart = cart_service.add_to_cart(serializer, logged_in_user)
        response = CartSerializer(cart).data
        return Response(response, status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quantities(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    serializer = UpdateQuantity(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        cart = cart_service.update_item_quantities(serializer, logged_in_user)
        response = CartSerializer(cart).data
        return Response(response, status=status.HTTP_200_OK)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_items(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    serializer = DeleteCartItems(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        cart = cart_service.delete_cart_items(serializer, logged_in_user)
        data = CartSerializer(cart).data
        return Response(data, status=status.HTTP_200_OK)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    cart = cart_service.clear_cart(logged_in_user)
    data = CartSerializer(cart).data
    return Response(data, status=status.HTTP_200_OK)

