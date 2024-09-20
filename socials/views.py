import logging

from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from socials.serializers import SocialUserSerializer, CreateUserSocials
from socials.social_service import SocialService

social_service = SocialService()

logger = logging.getLogger('django')


# Create your views here.
@api_view(['GET'])
def find_users_socials(request, uuid):
    queryset = social_service.find_users_socials(uuid)
    data = SocialUserSerializer(queryset, many=True).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_user_socials(request, uuid):
    serializer = CreateUserSocials(data=request.data, many=True)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        queryset = social_service.create_user_socials(uuid, serializer)
        data = SocialUserSerializer(queryset, many=True).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user_account(request, uuid: str, id: int):
    queryset = social_service.delete_user_social(uuid, id)
    data = SocialUserSerializer(queryset, many=True).data
    return Response(data)
