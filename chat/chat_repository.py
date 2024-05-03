from django.conf import settings
from .models import Room, Message

User = settings.AUTH_USER_MODEL


class ChatRepository:

    def join_room(self, user: User):
        pass

    def leave_room(self, user: User):
        pass

    def get_room_online_count(self):
        pass
