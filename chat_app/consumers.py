import asyncio
import json
from django.contrib.auth import get_user_model
from channels.consumer import AsyncConsumer
from channels.db import DatabaseSyncToAsync

from .models import (
    ChatModel,
    MessageModel,
    User,
    User2UnreadMessage,
    Chat2User,
)

class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print('connected', event)

    async def websocket_recieve(self, event):
        print('recieved', event)

    async def websocket_disconnect(self, event):
        print('disconnected', event)