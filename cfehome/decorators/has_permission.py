import logging
from functools import wraps
from typing import List
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.conf import settings

from auth.user_service import UserService

logger = logging.getLogger('django')
user_service = UserService()


def get_user_groups(username: str) -> List[Group]:
    user = user_service.find_user_by_username(username)
    logger.info(f'user: {user}')
    return user.groups


def has_permission(perm_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_groups = get_user_groups(request.user)
                for group in user_groups:
                    if group.permissions.filter(name=perm_name).exists():
                        return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("You don't have permission to access this page.")

        return _wrapped_view

    return decorator
