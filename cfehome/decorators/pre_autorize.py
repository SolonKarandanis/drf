import logging
from functools import wraps

from rest_framework.response import Response
from rest_framework import status
from rest_framework.request import Request

from cfehome.authorization import Condition

logger = logging.getLogger('django')


def pre_authorize(condition: Condition):
    """
    Decorator that evaluates a Condition before the view runs.

    Compose conditions with & (AND) and | (OR):

        @pre_authorize(HasRole(ADMIN))
        @pre_authorize(HasPermission(CHANGE_USER))
        @pre_authorize(HasPermission(CHANGE_USER) | SecurityCheck(security_service.is_user_me))
        @pre_authorize(HasPermission(CHANGE_PRODUCT) & SecurityCheck(security_service.is_product_mine))
        @pre_authorize(HasPermission(CHANGE_CART_ITEM) & SecurityCheckList(security_service.are_cart_items_mine, "cartItemId"))
    """
    def inner_decorator(function):
        @wraps(function)
        def wrapped(*args, **kwargs):
            request: Request = args[0]
            data = request.data
            logged_in_user = request.user

            if not condition.evaluate(request, logged_in_user, data, kwargs):
                return Response(status=status.HTTP_401_UNAUTHORIZED)
            return function(*args, **kwargs)

        return wrapped
    return inner_decorator
