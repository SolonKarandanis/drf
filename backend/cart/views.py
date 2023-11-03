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
    cart = Cart.objects.get_queryset().with_cart_items().owned_by(logged_in_user)
    data = CartSerializer(cart, many=False).data
    return Response(data)
