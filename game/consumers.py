from channels.generic.websocket import AsyncJsonWebsocketConsumer
import json
from asyncio import sleep
import random

class GameConsumer(AsyncJsonWebsocketConsumer):
    # async def connect(self):
    #     await self.accept()
        
    #     for _ in range(1000):
    #         await self.send(json.dumps({"message": random.randint(-20, 20)}))
    #         await sleep(1)
    
    
    async def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['room_code']
        await self.channel_layer.group_add(
            self.room_code,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_code,
            self.channel_name
        )
        
    async def receive_json(self, content):
        command = content.get("command", None)
        
        if command == "joined":
            await self.channel_layer.group_send(
                self.room_code,
                {
                    "type": "websocket_joined",
                    "user": content.get("user", None),
                    "command":command
                }
            )
            
        if command == "message":
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_code,
                {
                    'type': 'game_message',
                    'message': content.get("message", None),
                    "command":command
                }
            )

    # async def receive(self, text_data):
    #     text_data_json = json.loads(text_data)
    #     message = text_data_json['message']

    #     # Send message to room group
    #     await self.channel_layer.group_send(
    #         self.room_code,
    #         {
    #             'type': 'game_message',
    #             'message': message
    #         }
    #     )

    async def game_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
        
    async def websocket_joined(self, event):
        await self.send_json(({
             'command':event["command"],
             'user':event["user"]
        }))
