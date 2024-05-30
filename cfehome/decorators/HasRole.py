import logging

from rest_framework.permissions import BasePermission
from rest_framework.views import APIView

logger = logging.getLogger('django')


class HasRole(BasePermission):
    """
    Allows access only to admin users.
    """



    def has_object_permission(self, request, view, obj):
        logger.info(f'obj: {obj}')
        logger.info(f'request: {request}')
        return bool(request.user.is_authenticated)