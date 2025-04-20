
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class JobConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("jobs", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("jobs", self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        await self.channel_layer.group_send(
            "jobs",
            {
                'type': 'job_message',
                'message': message
            }
        )

    async def job_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
