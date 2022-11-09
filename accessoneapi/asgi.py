"""
ASGI config for accessoneapi project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from app.consumer import *

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'accessoneapi.settings')

application = get_asgi_application()

from app.routing import websocket_url_pattern

application= ProtocolTypeRouter(
    {
        'http' : application,
        'websocket':AuthMiddlewareStack(URLRouter(websocket_url_pattern))
    }
)