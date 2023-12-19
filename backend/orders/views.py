from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

import logging
from .models import Order
from .order_service import OrderService
from .serializers import OrderSerializer, OrderListSerializer

order_service = OrderService()

# Create your views here.
logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    orders = order_service.find_users_orders(logged_in_user)
    data = OrderListSerializer(orders, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, uuid):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_draft_orders(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    try:
        orders = order_service.place_draft_orders(logged_in_user)
        data = OrderSerializer(orders, many=True).data
        return Response(data)
    except Exception as error:
        logger.error(f'error: {error}')
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


