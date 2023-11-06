from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
import logging

# Create your views here.
from .models import Cart
from .serializers import CartSerializer

logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_cart(request):
    logged_in_user = request.user
    cart = Cart.objects.get_queryset()\
        .with_cart_items()\
        .owned_by(logged_in_user)\
        .get_or_create(total_price=0, user=logged_in_user)[0]
    logger.info(f'cart: {cart}')
    data = CartSerializer(cart).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_cart_items(request):
    pass


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_quantities(request):
    pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_cart_items(request):
    pass


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def clear_cart(request):
    pass