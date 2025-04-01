import inspect
import logging
import re
from functools import wraps

from requests import Response
from rest_framework import status
from rest_framework.request import Request

from cfehome.security_service import SecurityService
from cfehome.utils.security_utils import SecurityUtils

logger = logging.getLogger('django')

security_service = SecurityService()


def pre_authorize(value: str):
    def inner_decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            is_authorized = False
            request: Request = args[0]
            data = request.data
            logger.info(f'-----> request data {data}')
            parts_split_by_and = value.split('&&')
            for part in parts_split_by_and:
                trimmed_part = part.strip()
                has_permission_pattern = re.compile(r"(hasPermission)(.+)", re.IGNORECASE)
                has_permission_match = has_permission_pattern.match(trimmed_part)
                if has_permission_match:
                    permission = has_permission_match.group()[14:-1]
                    is_authorized = _check_user_permission(request, permission)
                has_role_pattern = re.compile(r"(hasRole)(.+)", re.IGNORECASE)
                has_role_match = has_role_pattern.match(trimmed_part)
                if has_role_match:
                    role = has_role_match.group()[8:-1]
                    is_authorized = _check_user_role(request, role)
                has_security_service_pattern = re.compile(r"securityService(.+)", re.IGNORECASE)
                has_security_service_match = has_security_service_pattern.match(trimmed_part)
                if has_security_service_match:
                    security_method_expression = has_security_service_match.group()
                    method = security_method_expression.split('.')[1]
                    splitted = method.split('(')
                    method_name = splitted[0]
                    method_arguments = splitted[1][:-1]
                    logger.info(f'-----> {method_name=}')
                    logger.info(f'-----> {method_arguments=}')
                    methods_list = [method for method in dir(security_service) if
                                    callable(getattr(security_service, method)) and not method.startswith('__')]
                    for method in methods_list:
                        if method == method_name:
                            func = getattr(security_service, method_name)
                            logger.info(f'  {method=} {func=}')
                            if type(data) == list and "[]" in method_arguments:
                                variable_name = method_arguments.split("[]")[0]
                                arg = [d[variable_name] for d in data]
                                is_authorized = security_service.execute_method(method_name, arg)

                    # attrs = (getattr(security_service, name) for name in dir(security_service))
                    # methods = filter(inspect.ismethod, attrs)
                    # for method in methods:
                    #     logger.info(f'  {vars(method)=}')

                    # for method in methods_list:
                    #     logger.info(f'  {type(method)=}')
                    # functions = inspect.getmembers(security_service, predicate=inspect.ismethod)
                    # for name, function in functions:
                    #     logger.info(f' {name=} {function=}')
                    #     if name == method_name:
                    #         is_authorized = True
                    #     sig = inspect.signature(function)
                    #     logger.info(f'Function "{name}" has a params {sig}')

            if not is_authorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            response = function(*args, **kwargs)
            return response

        return wrapped

    return inner_decorator


def _check_user_permission(request: Request, permission: str) -> bool:
    logged_in_user = request.user
    has_user_permission: bool = SecurityUtils.has_permission(request, permission)
    logger.info(
        f'-----> logged_in_user: {logged_in_user.username} -> has_permission: {permission} => {has_user_permission}')
    return has_user_permission


def _check_user_role(request: Request, role: str) -> bool:
    logged_in_user = request.user
    has_user_role: bool = SecurityUtils.has_role(request, role)
    logger.info(f'------> logged_in_user: {logged_in_user.username} -> has_role: {role} => {has_user_role}')
    return has_user_role
