"""
ASGI config for cfehome project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddleware, AuthMiddlewareStack
import notifications.routing
import chat.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cfehome.settings')
routes = [
    *notifications.routing.websocket_urlpatterns,
    *chat.routing.websocket_urlpatterns
]
django.setup()

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(routes)
    )
})
