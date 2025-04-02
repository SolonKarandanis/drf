import logging

import jwt
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import status
from rest_framework import serializers
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
from celery.result import AsyncResult

from cfehome.constants.security_constants import ADMIN, CHANGE_USER
from cfehome.decorators.pre_autorize import pre_authorize
from images.serializers import ImagesSerializer
from socials.social_service import SocialService
from .group_service import GroupService
from .models import User
from .serializers import PaginatedUserSerializer, CreateUserSerializer, UseInfoSerializer, GroupSerializer, \
    UserAccountSerializer, SearchUsersRequestSerializer, PaginatedPOSTUserSerializer, ChangeUserStatusSerializer, \
    UploadCVSerializer, UploadProfilePictureSerializer, UpldateUserContactInfoSerializer, UpdateBioSerializer, \
    ResetUserPasswordSerializer
from .tasks import create_task
from .user_service import UserService

logger = logging.getLogger('django')

user_service = UserService()
social_service = SocialService()
group_service = GroupService()


@api_view(['POST'])
@permission_classes([AllowAny])
def perform_login(request: Request):
    username = request.data.get("username")
    password = request.data.get("password")
    user_to_login = user_service.find_active_user(username)
    logger.info(f'----> Auth views ----> perform_login ----> user_to_login: {user_to_login}')
    if user_to_login is None:
        error_message = "This User Profile is not active"
        error_name = "not_active_profile"
        raise exceptions.AuthenticationFailed(error_message, error_name)

    authenticated_user = authenticate(username=username, password=password)
    if authenticated_user is None:
        error_message = "Authentication Failure"
        error_name = "error.auth"
        raise exceptions.AuthenticationFailed(error_message, error_name)

    refresh_token = RefreshToken.for_user(user_to_login)
    access_token = refresh_token.access_token

    decode_jwt = jwt.decode(str(access_token), settings.SECRET_KEY, algorithms=["HS256"])

    decode_jwt["email"] = user_to_login.email
    decode_jwt["username"] = user_to_login.username
    groups = user_service.find_user_groups(user_to_login)
    decode_jwt["groups"] = [group.name for group in groups]
    perm_list = user_to_login.get_group_permissions()
    decode_jwt["permissions"] = [perm for perm in perm_list]

    encoded = jwt.encode(decode_jwt, settings.SECRET_KEY, algorithm="HS256")

    return Response({
        'refresh': str(refresh_token),
        'access': str(encoded),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request: Request):
    queryset = user_service.find_all_users()
    serializer = PaginatedUserSerializer(queryset, request)
    return Response(serializer.page_data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search_users(request: Request):
    logged_in_user = get_user_from_request(request)
    search_request = SearchUsersRequestSerializer(data=request.data)
    if search_request.is_valid(raise_exception=True):
        serialized_data = search_request.data
        queryset = user_service.search(serialized_data, logged_in_user)
        paging = serialized_data["paging"]
        serializer = PaginatedPOSTUserSerializer(queryset, paging)
        return Response(serializer.page_data)


@api_view(['POST'])
def register_user(request: Request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        created_user = user_service.register_user(serializer)
        logger.info(f'----> Auth views ----> register_user ----> created_user: {created_user}')
        data = UseInfoSerializer(created_user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
@pre_authorize(f"hasRole({ADMIN})")
def activate_user_account(request: Request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_activated(user_uuid)
        user = user_service.find_user_by_uuid(user_uuid, True)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAdminUser])
@pre_authorize(f"hasRole({ADMIN})")
def deactivate_user_account(request: Request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_deactivated(user_uuid)
        user = user_service.find_user_by_uuid(user_uuid, True)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAdminUser])
@pre_authorize(f"hasRole({ADMIN})")
def delete_user_account(request: Request):
    serializer = ChangeUserStatusSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serialized_data = serializer.data
        user_uuid = serialized_data["userId"]
        user_service.user_account_status_deleted(user_uuid)
        user = user_service.find_user_by_uuid(user_uuid, True)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({CHANGE_USER})")
def reset_user_password(request: Request):
    logged_in_user = get_user_from_request(request)
    serializer = ResetUserPasswordSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user_service.reset_password(serializer, logged_in_user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request: Request, uuid):
    user = user_service.find_user_by_uuid(uuid, True)
    data = UseInfoSerializer(user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account(request: Request):
    user = get_user_from_request(request)
    data = UserAccountSerializer(user).data
    return Response(data)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_groups(request: Request):
    groups = group_service.find_all_groups()
    logger.info(f'---> Auth Views ---> groups: {groups}')
    data = GroupSerializer(groups, many=True).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_statuses(request: Request):
    statuses = user_service.get_user_statuses()
    return Response(statuses)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({CHANGE_USER}) && securityService.is_user_me(uuid)")
def upload_profile_image(request: Request, uuid):
    logged_in_user = get_user_from_request(request)
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
def get_user_image(request: Request, uuid):
    user_image = user_service.get_user_image(uuid)
    if user_image is None:
        return Response(status=status.HTTP_404_NOT_FOUND)
    data = ImagesSerializer(user_image).data
    return Response(data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({CHANGE_USER}) && securityService.is_user_me(uuid)")
def upload_cv(request: Request, uuid):
    logged_in_user = get_user_from_request(request)
    serializer = UploadCVSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        cv: InMemoryUploadedFile = request.FILES.get('cv')
        user_service.upload_cv(cv, uuid)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({CHANGE_USER}) && securityService.is_user_me(uuid)")
def update_user_contact_info(request: Request, uuid):
    logged_in_user = get_user_from_request(request)
    serializer = UpldateUserContactInfoSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = user_service.update_user_contact_info(uuid, serializer)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
@pre_authorize(f"hasPermission({CHANGE_USER}) && securityService.is_user_me(uuid)")
def update_user_bio(request: Request, uuid):
    logged_in_user = get_user_from_request(request)
    serializer = UpdateBioSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        user = user_service.update_user_bio(uuid, serializer)
        data = UseInfoSerializer(user).data
        return Response(data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def get_user_from_request(request: Request):
    logged_in_user = request.user
    logger.info(f'---> Auth Views ---> logged_in_user: {logged_in_user}')
    return logged_in_user


def is_user_me(logged_in_user: User, uuid: str):
    request_uuid = str(uuid)
    logged_in__user_uuid = str(logged_in_user.uuid)
    if request_uuid != logged_in__user_uuid:
        raise serializers.ValidationError({"not-allowed": "Action not allowed."})


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
