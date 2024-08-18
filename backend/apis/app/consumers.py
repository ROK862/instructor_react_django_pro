import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import FlexChats, User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_number = self.scope['url_route']['kwargs'].get('sender_number')
        self.receiver_number = self.scope['url_route']['kwargs'].get('receiver_number')

        # Allow connection
        await self.channel_layer.group_add(
            self.receiver_number,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove from group
        await self.channel_layer.group_discard(
            self.receiver_number,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json.get('message')

        sender = User.objects.get(phone_number=self.sender_number)
        receiver = User.objects.get(phone_number=self.receiver_number)

        # Save message to database
        chat = FlexChats(sender=sender, receiver=receiver, message=message)
        chat.save()

        # Send message to receiver
        await self.channel_layer.group_send(
            self.receiver_number,
            {
                'type': 'chat_message',
                'message': message,
                'id': chat.id
            }
        )

    async def chat_message(self, event):
        message = event['message']
        chat_id = event['id']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'id': chat_id
        }))