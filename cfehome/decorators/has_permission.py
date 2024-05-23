from functools import wraps
from typing import List
from django.http import HttpResponseForbidden
from django.contrib.auth.models import Group
from django.conf import settings

User = settings.AUTH_USER_MODEL


def get_user_groups(user_id: int) -> List[Group]:
    user = User.objects.get(id=user_id)
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
