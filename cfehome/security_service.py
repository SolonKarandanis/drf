import logging

from auth.group_service import GroupService
from auth.user_service import UserService

logger = logging.getLogger('django')

user_service = UserService()
group_service = GroupService()

class SecurityService:
    pass