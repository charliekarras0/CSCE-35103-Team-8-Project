from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/hud/', consumers.HUDConsumer.as_asgi()),  # URL for the WebSocket connection
]
