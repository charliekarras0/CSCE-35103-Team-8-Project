from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ScoreConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        # Handle incoming messages from WebSocket if needed
        pass

    async def send_score_update(self, red_team_score, blue_team_score, players):
        message = {
            'red_team_score': red_team_score,
            'blue_team_score': blue_team_score,
            'players': players,
        }
        await self.send(text_data=json.dumps(message))

    async def update_scores(self, red_team_score, blue_team_score, players):
        # Logic to update scores
        await self.send_score_update(red_team_score, blue_team_score, players)
