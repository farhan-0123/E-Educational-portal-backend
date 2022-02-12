"""
ASGI config for E_Educational_portal_backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from core.chat.routing import websockets_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'E_Educational_portal_backend.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websockets_urlpatterns
        )
    )
})
