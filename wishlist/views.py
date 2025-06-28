from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
import logging

from wishlist.serializers import WishListItemSerializer
from wishlist.wishlist_service import WishlistService

wishlist_service = WishlistService()

logger = logging.getLogger('django')


# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @pre_authorize(f"hasPermission({VIEW_CART})")
def get_user_wishlist_items(request: Request):
    logged_in_user = get_user_from_request(request)
    wishlist_items = wishlist_service.fetch_user_wish_list_items_dto(logged_in_user)
    data = WishListItemSerializer(wishlist_items, many=True).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
# @pre_authorize(f"hasPermission({ADD_CART_ITEM})")
def add_to_wishlist(request: Request):
    pass


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
# @pre_authorize(f"hasPermission({DELETE_CART_ITEM}) && securityService.are_cart_items_mine(cartItemId[])")
def remove_wishlist_item(request: Request):
    pass


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def add_item_to_cart(request: Request, uuid: str):
    pass


def get_user_from_request(request: Request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    return logged_in_user
