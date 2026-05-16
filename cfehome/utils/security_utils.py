from typing import List

import jwt
from django.conf import settings
import logging

logger = logging.getLogger('django')


class SecurityUtils:

    @staticmethod
    def get_token_from_request(request):
        return request.auth

    @staticmethod
    def get_claims_from_request(request):
        token = SecurityUtils.get_token_from_request(request)
        decoded_jwt = jwt.decode(str(token), settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_jwt

    @staticmethod
    def get_user_from_request(request):
        logged_in_user = request.user
        logger.info(f'---> Product Views ---> logged_in_user: {logged_in_user}')
        return logged_in_user

    @staticmethod
    def _get_permissions(decoded_jwt, request) -> list:
        # SimpleJWT's standard refresh endpoint returns a plain token without the
        # custom claims injected by perform_login. Fall back to the DB so that
        # @pre_authorize keeps working after a reactive token refresh.
        permissions = decoded_jwt.get('permissions')
        if permissions is None:
            permissions = list(request.user.get_group_permissions())
        return permissions

    @staticmethod
    def _get_roles(decoded_jwt, request) -> list:
        roles = decoded_jwt.get('groups')
        if roles is None:
            roles = list(request.user.groups.values_list('name', flat=True))
        return roles

    @staticmethod
    def has_permission(request, permission: str) -> bool:
        decoded_jwt = SecurityUtils.get_claims_from_request(request)
        permissions = SecurityUtils._get_permissions(decoded_jwt, request)
        return permission in permissions

    @staticmethod
    def has_role(request, role: str) -> bool:
        decoded_jwt = SecurityUtils.get_claims_from_request(request)
        roles = SecurityUtils._get_roles(decoded_jwt, request)
        return role in roles

    @staticmethod
    def has_any_permission(request, supplied_permissions: List[str]) -> bool:
        decoded_jwt = SecurityUtils.get_claims_from_request(request)
        permissions = SecurityUtils._get_permissions(decoded_jwt, request)
        return any(p in permissions for p in supplied_permissions)
