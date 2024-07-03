import logging

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from celery.result import AsyncResult

from socials.social_service import SocialService
from .group_service import GroupService
from .serializers import PaginatedUserSerializer, CreateUserSerializer, UseInfoSerializer, GroupSerializer, \
    UserAccountSerializer, SearchUsersRequestSerializer, PaginatedPOSTUserSerializer, ChangeUserStatusSerializer, \
    UploadCVSerializer, UploadProfilePictureSerializer
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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def activate_user_account(request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_activated(user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
def deactivate_user_account(request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_deactivated(user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user_account(request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_deleted(user_uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def email_check(user):
    # security service checks
    logger.info(f'user: {user}')
    return True


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request, uuid):
    user = user_service.find_user_by_uuid(uuid, True)
    data = UseInfoSerializer(user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account(request):
    user = get_user_from_request(request)
    data = UserAccountSerializer(user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_groups(request):
    groups = group_service.find_all_groups()
    logger.info(f'groups: {groups}')
    data = GroupSerializer(groups, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_statuses(request):
    statuses = user_service.get_user_statuses()
    return Response(statuses)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
# @permission_required("retrive_job", raise_exception=True)
# @permission_required({"retrive_job","retrive_job"}, raise_exception=True)
def upload_profile_image(request, uuid):
    logged_in_user = get_user_from_request(request)
    serializer = UploadProfilePictureSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        image: InMemoryUploadedFile = request.FILES.get('image')
        user_service.upload_profile_image(image, serializer, uuid, logged_in_user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_user_image(request,uuid):
    user = user_service.find_user_by_uuid(uuid)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_cv(request, uuid):
    serializer = UploadCVSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        cv: InMemoryUploadedFile = request.FILES.get('cv')
        user_service.upload_cv(cv, uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
