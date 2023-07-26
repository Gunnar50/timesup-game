from channels.generic.websocket import WebsocketConsumer
import json
from time import sleep
import random

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        
        for i in range(1000):
            self.send(json.dumps({"value": random.randint(-20, 20)}))
            sleep(1)
    
    
    # async def connect(self):
    #     self.room_code = self.scope['url_route']['kwargs']['room_code']
    #     await self.channel_layer.group_add(
    #         self.room_code,
    #         self.channel_name
    #     )
    #     await self.accept()

    # async def disconnect(self, close_code):
    #     await self.channel_layer.group_discard(
    #         self.room_code,
    #         self.channel_name
    #     )

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

    # async def game_message(self, event):
    #     message = event['message']

    #     # Send message to WebSocket
    #     await self.send(text_data=json.dumps({
    #         'message': message
    #     }))
