from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class ChatModel(models.Model):
    admin       = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    name        = models.CharField(max_length=50, null=True, blank=True)
    type        = models.CharField(max_length=2, default='u')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)


class MessageModel(models.Model):
    chat     = models.ForeignKey(ChatModel, on_delete=models.CASCADE)
    content     = models.TextField(null=False)
    datetime    = models.DateTimeField(null=False)
    sender   = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

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
