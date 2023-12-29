from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

import logging
from .models import Order
from .order_service import OrderService
from .serializers import OrderSerializer, OrderListSerializer, PostOrderComment, SearchOrderItems, OrderItemSerializer

order_service = OrderService()

# Create your views here.
logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    logged_in_user = get_user_from_request(request)
    orders = order_service.find_users_orders(logged_in_user)
    data = OrderListSerializer(orders, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, uuid):
    logged_in_user = get_user_from_request(request)
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_draft_orders(request):
    logged_in_user = get_user_from_request(request)
    try:
        orders = order_service.place_draft_orders(logged_in_user)
        data = OrderSerializer(orders, many=True).data
        return Response(data)
    except Exception as error:
        logger.error(f'error: {error}')
        return Response(str(error), status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def post_order_comment(request):
    logged_in_user = get_user_from_request(request)
    serializer = PostOrderComment(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        order = order_service.post_order_comment(serializer, logged_in_user)
        response = OrderSerializer(order, many=False).data
        return Response(response, status=status.HTTP_200_OK)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_buyer_rejected(request, uuid):
    logged_in_user = get_user_from_request(request)
    order_service.change_order_status_to_buyer_rejected(uuid)
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_supplier_rejected(request, uuid):
    logged_in_user = get_user_from_request(request)
    order_service.change_order_status_to_supplier_rejected(uuid)
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_approved(request, uuid):
    logged_in_user = get_user_from_request(request)
    order_service.change_order_status_to_approved(uuid)
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_shipped(request, uuid):
    logged_in_user = get_user_from_request(request)
    order_service.change_order_status_to_shipped(uuid)
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def order_received(request, uuid):
    logged_in_user = get_user_from_request(request)
    order_service.change_order_status_to_received(uuid)
    order: Order = order_service.find_order_by_uuid(uuid)
    data = OrderSerializer(order, many=False).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_order_items(request):
    logged_in_user = get_user_from_request(request)
    serializer = SearchOrderItems(data=request.data, many=False)
    if serializer.is_valid(raise_exception=True):
        query = serializer.data
        search_results = order_service.search_order_items(query, logged_in_user)
        logger.info(f'search_results: {search_results}')
        response = OrderItemSerializer(search_results, many=True).data
        return Response(response, status=status.HTTP_200_OK)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


def get_user_from_request(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    return logged_in_user
