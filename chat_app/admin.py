from django.contrib import admin

from .models import ChatModel, MessageModel, Chat2User

# Register your models here.

admin.site.register(ChatModel)
admin.site.register(MessageModel)
admin.site.register(Chat2User)
