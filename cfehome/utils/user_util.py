from typing import List

from django.contrib.auth.models import Group, Permission

from auth.models import User


class UserUtil:

    @staticmethod
    def get_user_roles(user: User) -> List[Group]:
        return user.groups

    @staticmethod
    def get_user_permissions(user: User) -> List[Permission]:
        return user.user_permissions

    @staticmethod
    def has_role(user: User, role: str) -> bool:
        user_groups = UserUtil.get_user_roles(user)
        if user_groups.filter(name=role).exists():
            return True
        return False

    @staticmethod
    def has_permission(user: User, permission: str) -> bool:
        if user.has_perm(permission):
            return True
        return False
