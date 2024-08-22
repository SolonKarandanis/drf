import logging
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

logger = logging.getLogger('django')


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_payment_cards(request):
    pass


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_card(request):
    pass


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_payment_card(request):
    pass
