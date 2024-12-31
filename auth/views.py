import logging

from django.core.files.uploadedfile import InMemoryUploadedFile
from rest_framework import status
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from celery.result import AsyncResult

from images.serializers import ImagesSerializer
from socials.social_service import SocialService
from .group_service import GroupService
from .models import User
from .serializers import PaginatedUserSerializer, CreateUserSerializer, UseInfoSerializer, GroupSerializer, \
    UserAccountSerializer, SearchUsersRequestSerializer, PaginatedPOSTUserSerializer, ChangeUserStatusSerializer, \
    UploadCVSerializer, UploadProfilePictureSerializer, UpldateUserContactInfoSerializer, UpdateBioSerializer, \
    LoginSerializer
from .tasks import create_task
from .user_service import UserService

logger = logging.getLogger('django')

user_service = UserService()
social_service = SocialService()
group_service = GroupService()


# Create your views here.
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


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
def register_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        created_user =user_service.register_user(serializer)
        logger.info(f'----> Auth views ----> register_user ----> created_user: {created_user}')
        data = UseInfoSerializer(created_user).data
        return Response(data)
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
    logger.info(f'---> Auth Views ---> groups: {groups}')
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
    is_user_me(logged_in_user, uuid)
    serializer = UploadProfilePictureSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        image: InMemoryUploadedFile = request.FILES.get('image')
        user_service.upload_profile_image(image, serializer, logged_in_user)
        user_image = user_service.get_user_image(uuid)
        data = ImagesSerializer(user_image).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_image(request, uuid):
    user_image = user_service.get_user_image(uuid)
    if user_image is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ImagesSerializer(user_image).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_cv(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    serializer = UploadCVSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        cv: InMemoryUploadedFile = request.FILES.get('cv')
        user_service.upload_cv(cv, uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_contact_info(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    serializer = UpldateUserContactInfoSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = user_service.update_user_contact_info(uuid, serializer)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_bio(request, uuid):
    logged_in_user = get_user_from_request(request)
    is_user_me(logged_in_user, uuid)
    serializer = UpdateBioSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = user_service.update_user_bio(uuid, serializer)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user_from_request(request):
    logged_in_user = request.user
    logger.info(f'---> Auth Views ---> logged_in_user: {logged_in_user}')
    return logged_in_user


def is_user_me(logged_in_user: User, uuid: str):
    request_uuid = str(uuid)
    logged_in__user_uuid = str(logged_in_user.uuid)
    if request_uuid != logged_in__user_uuid:
        raise serializers.ValidationError({"not-allowed":"Action not allowed."})


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
