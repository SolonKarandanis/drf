import logging
from functools import wraps
from typing import List
from django.http import HttpResponseForbidden
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


def has_role(role: str):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            request: Request = args[0]
            has_user_role: bool = SecurityUtils.has_role(request, role)
            logger.info(f'-----> has_role: {has_user_role}')
            if not has_user_role:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            response = f(*args, **kwargs)
            return response

        return wrapped

    return inner_decorator
