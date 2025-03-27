import logging
import re

from requests import Response
from rest_framework import status
from rest_framework.request import Request

from cfehome.utils.security_utils import SecurityUtils

logger = logging.getLogger('django')


def pre_authorize(value: str):
    def inner_decorator(f):
        def wrapped(*args, **kwargs):
            is_authorized = False
            request: Request = args[0]
            has_permission_pattern = re.compile(r"(hasPermission)(.+)", re.IGNORECASE)
            has_permission_match = has_permission_pattern.match(value)
            if has_permission_match:
                permission = has_permission_match.group()[14:-1]
                is_authorized = _check_user_permission(request, permission)
            has_role_pattern = re.compile(r"(hasRole)(.+)", re.IGNORECASE)
            has_role_match = has_role_pattern.match(value)
            if has_role_match:
                role = has_role_match.group()[8:-1]
                is_authorized = _check_user_role(request, role)
            if not is_authorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            response = f(*args, **kwargs)
            return response

        return wrapped

    return inner_decorator


def _check_user_permission(request: Request, permission: str) -> bool:
    has_user_permission: bool = SecurityUtils.has_permission(request, permission)
    logger.info(f'-----> has_user_permission: {permission} => {has_user_permission}')
    return has_user_permission


def _check_user_role(request: Request, role: str) -> bool:
    has_user_role: bool = SecurityUtils.has_role(request, role)
    logger.info(f'-----> has_user_role: {role} => {has_user_role}')
    return has_user_role