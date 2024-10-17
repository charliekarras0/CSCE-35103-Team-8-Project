# consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class HUDConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join the 'hud_updates' group
        self.group_name = "hud_updates"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def send_score_update(self, event):
        scores = event['scores']
        print(f"Received scores in WebSocket: {scores}")  # Debug print
        
        # Send the score update to the WebSocket
        await self.send(text_data=json.dumps({
            'type': 'score_update',
            'scores': scores,
        }))
