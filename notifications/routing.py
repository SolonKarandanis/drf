from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'notification/(?P<user_uuid>[0-9a-f-]{36})/$', consumers.NotificationConsumer.as_asgi()),
]