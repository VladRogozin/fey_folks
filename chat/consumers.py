import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Chat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        message = json.loads(text_data)
        sender = message['sender']
        content = message['content']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'sender': sender,
                'content': content,
                'avatar': self.scope['user'].avatar.url  # Передача URL аватара
            }
        )

        # Create and save the message to the database
        chat = await self.get_chat_instance()
        await self.save_message(content, sender, chat)

    @database_sync_to_async
    def get_chat_instance(self):
        return Chat.objects.get(chat_name=self.room_name)

    @database_sync_to_async
    def save_message(self, content, sender, chat):
        Message.objects.create(content=content, sender=self.scope['user'], chat=chat)

    async def chat_message(self, event):
        sender = event['sender']
        content = event['content']
        avatar = event['avatar']  # Получение URL аватара из события

        await self.send(text_data=json.dumps({
            'sender': sender,
            'content': content,
            'avatar': avatar  # Передача URL аватара в событии
        }))
