from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from rest_framework.request import Request

from cfehome.utils.security_utils import SecurityUtils


class Condition:
    def __and__(self, other: Condition) -> AndCondition:
        return AndCondition(self, other)

    def __or__(self, other: Condition) -> OrCondition:
        return OrCondition(self, other)

    def evaluate(self, request: Request, logged_in_user, data, kwargs: dict) -> bool:
        raise NotImplementedError


@dataclass
class HasPermission(Condition):
    permission: str

    def evaluate(self, request, logged_in_user, data, kwargs) -> bool:
        return SecurityUtils.has_permission(request, self.permission)


@dataclass
class HasRole(Condition):
    role: str

    def evaluate(self, request, logged_in_user, data, kwargs) -> bool:
        return SecurityUtils.has_role(request, self.role)


@dataclass
class SecurityCheck(Condition):
    """Calls a SecurityService method with logged_in_user + URL kwargs."""
    method: Callable

    def evaluate(self, request, logged_in_user, data, kwargs) -> bool:
        return self.method(logged_in_user=logged_in_user, **kwargs)


@dataclass
class SecurityCheckList(Condition):
    """Extracts a field from each request body item and passes it as arg= to the method."""
    method: Callable
    field: str

    def evaluate(self, request, logged_in_user, data, kwargs) -> bool:
        arg = [item[self.field] for item in data]
        return self.method(logged_in_user=logged_in_user, arg=arg, **kwargs)


@dataclass
class AndCondition(Condition):
    left: Condition
    right: Condition

    def evaluate(self, request, logged_in_user, data, kwargs) -> bool:
        return (self.left.evaluate(request, logged_in_user, data, kwargs)
                and self.right.evaluate(request, logged_in_user, data, kwargs))


@dataclass
class OrCondition(Condition):
    left: Condition
    right: Condition

    def evaluate(self, request, logged_in_user, data, kwargs) -> bool:
        return (self.left.evaluate(request, logged_in_user, data, kwargs)
                or self.right.evaluate(request, logged_in_user, data, kwargs))
