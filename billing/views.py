import logging
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from auth.models import User

logger = logging.getLogger('django')


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_users_payment_cards(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_card(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def edit_payment_card(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def selected_user_card(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)


def get_user_from_request(request):
    logged_in_user = request.user
    logger.info(f'----->logged_in_user: {logged_in_user}')
    return logged_in_user


def is_user_me(logged_in_user: User, uuid: str):
    request_uuid = str(uuid)
    logged_in__user_uuid = str(logged_in_user.uuid)
    if request_uuid != logged_in__user_uuid:
        raise serializers.ValidationError(f"Action Not Allowed")
