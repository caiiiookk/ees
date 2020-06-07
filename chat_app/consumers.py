import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import DatabaseSyncToAsync
from django.shortcuts import reverse

from .models import (
    ChatModel,
    MessageModel,
    User,
    User2UnreadMessage,
    Chat2User,
)

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):

        self.this_user = self.scope['user']
        chat_type = self.scope['url_route']['kwargs']['chat_type']
        chat_id = self.scope['url_route']['kwargs']['chat_id']

        if chat_type == 'u':
            self.other_user = await self.get_user_from_id_or_none(chat_id)
            self.this_chat = await self.get_user_chat(self.this_user, self.other_user)
            
        elif chat_type == 'g':
            pass
        elif chat_type == 'c':
            pass
        else:
            pass

        self.chat_room = chat_type + '_' + str(self.this_chat.id)
        await self.channel_layer.group_add(
            self.chat_room,
            self.channel_name
        )

        await self.send({
            'type': 'websocket.accept'
        })


    async def websocket_receive(self, event):
        event_text = event.get('text', None)
        if event_text is not None:
            loaded_message_dict = json.loads(event_text)
            msg_text = loaded_message_dict['message']
            db_msg = await self.send_message(msg_text)
            send_data = await self.form_text_answer(db_msg)
            print(self.chat_room)
            await self.channel_layer.group_send(
                self.chat_room, 
                {
                    'type': 'chat_message',
                    'text': send_data,
                }
            )
    
    async def chat_message(self, event):
        await self.send({
            'type': 'websocket.send',
            'text': event['text']
        })

    async def websocket_disconnect(self, event):
        print('disconnected', event)

    @DatabaseSyncToAsync
    def get_user_chat(self, this_user, other_user):
        return ChatModel.objects.get_or_create_user_chat(this_user, other_user)

    @DatabaseSyncToAsync
    def get_user_from_id_or_none(self, id):
        try:
            return User.objects.get(id=id)
        except:
            return None
    
    @DatabaseSyncToAsync
    def send_message(self, message):
        return MessageModel.objects.create_new_message(self.this_chat, self.this_user, message)

    @DatabaseSyncToAsync
    def form_text_answer(self, db_msg):
        user_profile_url = reverse('users_app:profile', kwargs={'id': db_msg.sender.id})
        return json.dumps({
                    'avatar_url': db_msg.sender.eesuser.avatar.url,
                    'user_profile_url': user_profile_url,
                    'sender_username': db_msg.sender.username,
                    'send_time': str(db_msg.datetime),
                    'message': db_msg.content
                    }
                )