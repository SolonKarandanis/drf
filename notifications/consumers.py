import json
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()


def _get_token_from_scope(scope) -> str | None:
    for header_name, header_value in scope.get('headers', []):
        if header_name == b'authorization':
            parts = header_value.decode().split()
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                return parts[1]
    return None


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user_uuid = self.scope['url_route']['kwargs']['user_uuid']
        token_str = _get_token_from_scope(self.scope)

        if not token_str:
            await self.close(code=4001)
            return

        try:
            token = AccessToken(token_str)
            user = await User.objects.aget(pk=token['user_id'])
        except (InvalidToken, TokenError, User.DoesNotExist, KeyError):
            await self.close(code=4001)
            return

        if str(user.uuid) != user_uuid:
            await self.close(code=4001)
            return

        self.group_name = f'notification_{user_uuid}'
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps(event['message']))
