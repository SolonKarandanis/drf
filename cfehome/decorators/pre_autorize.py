import inspect
import logging
import re
from functools import wraps

from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from cfehome.security_service import SecurityService
from cfehome.utils.security_utils import SecurityUtils

logger = logging.getLogger('django')

security_service = SecurityService()


def _evaluate_condition(trimmed_part: str, request: Request, logged_in_user, data, kwargs) -> bool:
    """Evaluate a single atomic condition and return True/False."""
    has_permission_pattern = re.compile(r"(hasPermission)(.+)", re.IGNORECASE)
    has_permission_match = has_permission_pattern.match(trimmed_part)
    if has_permission_match:
        permission = has_permission_match.group()[14:-1]
        return _check_user_permission(request, permission)

    has_role_pattern = re.compile(r"(hasRole)(.+)", re.IGNORECASE)
    has_role_match = has_role_pattern.match(trimmed_part)
    if has_role_match:
        role = has_role_match.group()[8:-1]
        return _check_user_role(request, role)

    has_security_service_pattern = re.compile(r"securityService(.+)", re.IGNORECASE)
    has_security_service_match = has_security_service_pattern.match(trimmed_part)
    if has_security_service_match:
        security_method_expression = has_security_service_match.group()
        method = security_method_expression.split('.')[1]
        splitted = method.split('(')
        method_name = splitted[0]
        method_arguments = splitted[1][:-1]
        methods_list = [m for m in dir(security_service) if
                        callable(getattr(security_service, m)) and not m.startswith('__')]
        for method in methods_list:
            if method == method_name:
                if type(data) == list and "[]" in method_arguments:
                    variable_name = method_arguments.split("[]")[0]
                    arg = [d[variable_name] for d in data]
                    return security_service.execute_method(method_name,
                                                          logged_in_user=logged_in_user,
                                                          arg=arg,
                                                          **kwargs)
                else:
                    return security_service.execute_method(method_name,
                                                          logged_in_user=logged_in_user,
                                                          method_arguments=method_arguments,
                                                          **kwargs)
        return False  # named method not found on SecurityService

    return False  # unrecognised condition → deny


def pre_authorize(value: str):
    """
    Decorator that evaluates a boolean expression before the view runs.

    Supported operators (standard precedence: && binds tighter than ||):
        hasPermission(<perm>)
        hasRole(<role>)
        securityService.<method>(<arg>)
        A && B   — both A and B must be true
        A || B   — either A or B must be true
        A && B || C   — (A && B) OR C

    Examples:
        @pre_authorize("hasRole(admin)")
        @pre_authorize("hasPermission(change_user) || securityService.is_user_me(uuid)")
        @pre_authorize("hasPermission(change_product) && securityService.is_product_mine(uuid)")
    """
    def inner_decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            request: Request = args[0]
            data = request.data
            logged_in_user = request.user

            # Split on || to get OR-groups; within each group split on && for AND-conditions.
            # access is granted when ANY or-group has ALL its and-conditions satisfied.
            or_groups = [g.strip() for g in value.split('||')]
            authorized = any(
                all(
                    _evaluate_condition(cond.strip(), request, logged_in_user, data, kwargs)
                    for cond in or_group.split('&&')
                    if cond.strip()
                )
                for or_group in or_groups
                if or_group
            )

            if not authorized:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return function(*args, **kwargs)

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
