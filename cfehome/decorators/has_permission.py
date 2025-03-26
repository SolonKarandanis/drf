import logging
from typing import List
from django.contrib.auth.models import Group
from requests import Response
from rest_framework import status
from rest_framework.request import Request

from auth.user_service import UserService
from cfehome.utils.security_utils import SecurityUtils

logger = logging.getLogger('django')
user_service = UserService()


def get_user_groups(username: str) -> List[Group]:
    user = user_service.find_user_by_username(username)
    logger.info(f'user: {user}')
    return user.groups


def has_permission(permission: str):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            request: Request = args[0]
            has_user_permission: bool = SecurityUtils.has_permission(request, permission)
            logger.info(f'-----> has_user_permission: {has_user_permission}')
            if not has_user_permission:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            response = f(*args, **kwargs)
            return response

        return wrapped

    return inner_decorator
