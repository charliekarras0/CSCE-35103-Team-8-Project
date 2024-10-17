"""
ASGI config for team8proj project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from lasertag import routing  # Import your app's routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'team8proj.settings')

# Create the ASGI application
application = ProtocolTypeRouter({
    "http": get_asgi_application(),  # For HTTP requests
    # Add WebSocket handling
    "websocket": AuthMiddlewareStack(
        URLRouter(
            routing.websocket_urlpatterns  # URL patterns for WebSocket connections
        )
    ),
})
