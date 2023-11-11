from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

import logging
from .models import Order

# Create your views here.
logger = logging.getLogger('django')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_orders(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request, pk):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def place_order(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
