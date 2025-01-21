from rest_framework import permissions
import logging

logger = logging.getLogger('django')


class IsProductMine(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            # Allow read-only methods for everyone
            logger.info(f'---> Product Permisions ---> IsProductMine ---> is_safe: True')
            return True
        # Check if the user making the request is the owner of the object
        is_mine = obj.user == request.user
        logger.info(f'---> Product Permisions ---> IsProductMine ---> is_mine: {is_mine}')
        return is_mine
