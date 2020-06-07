from django.urls import path

from .views import (
    ChatMainView,
    OpenChatView,
)

app_name = 'chat_app'

urlpatterns = [
    path('', ChatMainView.as_view(), name='main_chat_url'),
    path('<str:chat_type>/<int:chat_id>/', OpenChatView.as_view(), name='chat_url'),
]