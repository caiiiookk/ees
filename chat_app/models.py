from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Q

# Create your models here.


class ChatManager(models.Manager):    
    def get_or_create_user_chat(self, this_user, other_user):
        this_chat = ChatModel.objects.filter(chat2user__user=this_user).intersection(ChatModel.objects.filter(chat2user__user=other_user))
        if this_chat.__len__() == 0:
            this_chat = ChatModel.objects.create(type='u', created_at=datetime.utcnow())
            Chat2User.objects.create(chat=this_chat, user=this_user, activated=True, created=datetime.utcnow())
            Chat2User.objects.create(chat=this_chat, user=other_user, activated=False, created=datetime.utcnow())
        else:
            this_chat = this_chat[0]
        return this_chat


class ChatModel(models.Model):
    admin       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name        = models.CharField(max_length=50, null=True, blank=True)
    type        = models.CharField(max_length=2, default='u')
    created_at  = models.DateTimeField(auto_now_add=True)

    objects = ChatManager()

    def __str__(self):
        return str(self.id)

    
class MessageManager(models.Manager):
    def create_new_message(self, chat, sender, content):
        message = self.create(chat=chat, sender=sender, datetime=datetime.utcnow(), content=content)
        chat_users = self.get_chat_users(chat)
        for user in chat_users:
            Chat2User.objects.filter(user=user).update(activated=True)
        chat_users_except_this_user = chat_users.filter(~Q(id=sender.id))
        User2UnreadMessage.objects.bulk_create(
            [User2UnreadMessage(message=message, user=user) for user in chat_users_except_this_user]
        )
        return message

    def get_chat_users(self, chat):
        return User.objects.filter(chat2user__in=Chat2User.objects.filter(chat=chat))


class MessageModel(models.Model):
    chat     = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    content     = models.TextField(null=False)
    datetime    = models.DateTimeField(null=False)
    sender   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    objects = MessageManager()

    def __str__(self):
        return self.sender.username


class User2UnreadMessage(models.Model):
    user    = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(MessageModel, on_delete=models.CASCADE)


class Chat2User(models.Model):
    chat        = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    activated   = models.BooleanField(default=False)
    created     = models.DateTimeField(default=None, null=True)

    def __str__(self):
        return str(self.chat.id)
