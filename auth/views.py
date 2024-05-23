import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from celery.result import AsyncResult

from .group_service import GroupService
from .models import User
from .serializers import PaginatedUserSerializer, CreateUserSerializer, UserDetailSerializer, GroupSerializer, \
    UserAccountSerializer
from .tasks import create_task
from .user_service import UserService

logger = logging.getLogger('django')

user_service = UserService()
group_service = GroupService()


# Create your views here.

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    queryset = user_service.find_all_users()
    serializer = PaginatedUserSerializer(queryset, request)
    return Response(serializer.page_data)


@api_view(['POST'])
def create_user(request):
    serializer = CreateUserSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({"invalid": "not good data"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
# @has_permission('retrive_job')
def get_user(request, pk):
    obj = user_service.find_user_by_id(pk)
    data = UserDetailSerializer(obj).data
    return Response(data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_account(request):
    data = UserAccountSerializer(request.user).data
    return Response(data)


@api_view(['GET'])
def get_all_groups(request):
    groups = group_service.find_all_groups()
    logger.info(f'groups: {groups}')
    data = GroupSerializer(groups, many=True).data
    return Response(data)


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
