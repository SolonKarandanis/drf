import logging

from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from auth.models import User
from socials.serializers import SocialUserSerializer, CreateUserSocials, DeleteSocialUserItems, SocialSerializer
from socials.social_service import SocialService

social_service = SocialService()

logger = logging.getLogger('django')


# Create your views here.
@api_view(['GET'])
def find_all_socials(request):
    queryset = social_service.find_all_socials()
    data = SocialSerializer(queryset, many=True).data
    return Response(data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def find_users_socials(request, uuid):
    queryset = social_service.find_users_socials(uuid)
    data = SocialUserSerializer(queryset, many=True).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_user_socials(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    serializer = CreateUserSocials(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        queryset = social_service.create_user_socials(uuid, serializer)
        data = SocialUserSerializer(queryset, many=True).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def delete_user_social(request, uuid: str, id: int):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    queryset = social_service.delete_user_social(uuid, id)
    data = SocialUserSerializer(queryset, many=True).data
    return Response(data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def delete_user_social_by_ids(request, uuid: str):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    serializer = DeleteSocialUserItems(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        queryset = social_service.delete_user_socials(uuid, serializer)
        data = SocialUserSerializer(queryset, many=True).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_all_user_socials(request, uuid: str):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    social_service.delete_all_user_socials(uuid)
    return Response(status=status.HTTP_204_NO_CONTENT)


def get_user_from_request(request):
    logged_in_user = request.user
    logger.info(f'----->logged_in_user: {logged_in_user}')
    return logged_in_user


def is_user_me(logged_in_user: User, uuid: str):
    request_uuid = str(uuid)
    logged_in__user_uuid = str(logged_in_user.uuid)
    if request_uuid != logged_in__user_uuid:
        raise serializers.ValidationError(f"Action Not Allowed")
