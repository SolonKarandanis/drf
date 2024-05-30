import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from celery.result import AsyncResult

from cfehome.constants.security_constants import ADMIN
from cfehome.decorators.HasRole import HasRole
from cfehome.decorators.has_role import has_role
from socials.social_service import SocialService
from .group_service import GroupService
from .serializers import PaginatedUserSerializer, CreateUserSerializer, UseInfoSerializer, GroupSerializer, \
    UserAccountSerializer, SearchUsersRequestSerializer, PaginatedPOSTUserSerializer, ChangeUserStatusSerializer
from .tasks import create_task
from .user_service import UserService

logger = logging.getLogger('django')

user_service = UserService()
social_service = SocialService()
group_service = GroupService()


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    queryset = user_service.find_all_users()
    serializer = PaginatedUserSerializer(queryset, request)
    return Response(serializer.page_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_users(request):
    logged_in_user = get_user_from_request(request)
    search_request = SearchUsersRequestSerializer(data=request.data)
    if search_request.is_valid(raise_exception=True):
        serialized_data = search_request.data
        queryset = user_service.search(serialized_data, logged_in_user)
        paging = serialized_data["paging"]
        serializer = PaginatedPOSTUserSerializer(queryset, paging)
        return Response(serializer.page_data)


@api_view(['POST'])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def activate_user_account(request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_activated(user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def deactivate_user_account(request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_deactivated(user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user_account(request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_deleted(user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permission('retrive_job')
def get_user(request, uuid):
    user = user_service.find_user_by_uuid(uuid)
    s = social_service.find_users_socials(user)
    logger.info(f's: {s}')
    data = UseInfoSerializer(user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account(request):
    user = get_user_from_request(request)
    s = social_service.find_users_socials(user)
    data = UserAccountSerializer(user).data
    return Response(data)


@api_view(['GET'])
def get_all_groups(request):
    groups = group_service.find_all_groups()
    logger.info(f'groups: {groups}')
    data = GroupSerializer(groups, many=True).data
    return Response(data)


def get_user_from_request(request):
    logged_in_user = request.user
    logger.info(f'logged_in_user: {logged_in_user}')
    return logged_in_user


@api_view(['POST'])
def run_task(request):
    task_type = request.data['type']
    task = create_task.delay(int(task_type))
    return Response({"task_id": task.id}, status=202)


@api_view(['GET'])
def get_status(request, task_id):
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return Response(result, status=200)
