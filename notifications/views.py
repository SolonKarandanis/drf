import logging
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework import status

from .notification_repository import NotificationRepository
from .serializers import NotificationEventSerializer, MarkAsReadSerializer

logger = logging.getLogger('django')
notification_repo = NotificationRepository()


class NotificationCursorPagination(CursorPagination):
    page_size = 10
    ordering = '-created_at'


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    qs = notification_repo.find_unread_for_user(request.user)
    paginator = NotificationCursorPagination()
    page = paginator.paginate_queryset(qs, request)
    serializer = NotificationEventSerializer(page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_unread_count(request):
    count = notification_repo.count_unread_for_user(request.user)
    return Response({'count': count})


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def mark_as_read(request):
    serializer = MarkAsReadSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        notification_repo.mark_as_read(request.user, serializer.validated_data['ids'])
        return Response(status=status.HTTP_204_NO_CONTENT)
