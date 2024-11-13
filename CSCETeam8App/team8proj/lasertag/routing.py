from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/scores/', consumers.ScoreConsumer.as_asgi()), #URL for the WebSocket connection
]
