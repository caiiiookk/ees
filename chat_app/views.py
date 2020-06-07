from django.shortcuts import reverse, render, redirect, Http404
from django import views
from .models import (
    MessageModel,
    Chat2User,
    ChatModel,
    User,
    User2UnreadMessage,
)
from datetime import datetime
from django.db.models import Q

# Create your views here.

app_name = 'chat_app'


def form_chats_list(user):
    from django.db.models import Max
    from django.db.models.functions import Greatest
    user_chats = ChatModel.objects.filter(
        chat2user__user=user,
        chat2user__activated=True
    ).annotate(
            latest_activity_at=Greatest(
            'created_at',
            Max('messagemodel__datetime'),
        )
    ).order_by('-latest_activity_at')
    chats = []
    for chat in user_chats:
        name = None
        last_message = None
        link = None
        avatar = None
        if chat.type == 'u':
            other_user = User.objects.get(chat2user=Chat2User.objects.get(~Q(user=user), chat=chat))
            name = other_user.username
            link = reverse('chat_app:chat_url', kwargs={'chat_type': 'u', 'chat_id': other_user.id})
            avatar = other_user.eesuser.avatar.url
        else:
            name = chat.name
            avatar = '/media/no_img.png'
            link = '/chat/'
        last_message = MessageModel.objects.filter(chat=chat).order_by('datetime').last()
        my_chat = {
            'name': name,
            'last_message': last_message,
            'link': link,
            'avatar': avatar,
            'chat': chat,
        }
        chats.append(my_chat)
    return chats


class ChatMainView(views.View):
    def get(self, request):
        if not request.user.is_authenticated:
            raise Http404
        chats = ChatModel.objects.filter(chat2user__in=Chat2User.objects.filter(user=request.user))
        chatlist = []
        for chat in chats:
            chat_type = getattr(chat, 'type')
            chat_name = getattr(chat, 'name')
            chat_last_message = MessageModel.objects.filter(chat=chat).order_by('-datetime').first()
            if chat_type == 'u':
                chat_info = Chat2User.objects.filter(chat=chat).get(~Q(user=request.user))
                chat_user = getattr(chat_info, 'user')
                chat_name = getattr(chat_user, 'username')
                chat_avatar = getattr(chat_user.eesuser, 'avatar')
            elif chat_type == 'c':
                chat_avatar = '/media/no_img.png'
            else:
                chat_avatar = '/media/no_img.png'

            unread_messages = User2UnreadMessage.objects.filter(user=request.user).count()
            chatlist.append({
                'name': chat_name,
                'last_message': chat_last_message,
                'unread_messages': unread_messages,
                'avatar': chat_avatar,
                'id': getattr(chat, 'id'),
            })
        context = {
            'chats': chatlist,
            'chats_list': form_chats_list(request.user),
        }
        return render(request, 'chat/index.html', context)


class OpenChatView(views.View):
    def get(self, request, chat_type, chat_id):
        if chat_type == 'u':
            try:
                requested_user = User.objects.get(id=chat_id)
            except:
                raise Http404

            this_chat = ChatModel.objects.filter(chat2user__user=request.user).intersection(ChatModel.objects.filter(chat2user__user=requested_user))
            if this_chat.__len__() == 0:
                this_chat = ChatModel.objects.create(type='u', created_at=datetime.utcnow())
                Chat2User.objects.create(chat=this_chat, user=request.user, activated=True, created=datetime.utcnow())
                Chat2User.objects.create(chat=this_chat, user=requested_user, activated=False, created=datetime.utcnow())
            else:
                this_chat = this_chat[0]
            chat_messages = MessageModel.objects.filter(chat=this_chat).order_by('-datetime')
            context = {
                'other_user': requested_user,
                'chats_list': form_chats_list(request.user),
                'chat_messages': chat_messages,
                'this_chat': this_chat,
            }
            return render(request, 'chat/user_chat.html', context)
        elif chat_type == 'c':
            pass
        elif chat_type == 'g':
            pass
        raise Http404

    def post(self, request, chat_type, chat_id):
        if chat_type == 'u':
            try:
                requested_user = User.objects.get(id=chat_id)
            except:
                raise Http404

            this_chat = ChatModel.objects.filter(chat2user__user=request.user).intersection(ChatModel.objects.filter(chat2user__user=requested_user))
            if this_chat.__len__() == 0:
                raise Http404
            else:
                this_chat = this_chat[0]
            if request.POST['message']:
                MessageModel.objects.create(chat=this_chat, content=request.POST['message'], sender=request.user, datetime=datetime.utcnow())
                #Create unread msg for all other usrs

            return redirect('chat_app:chat_url', chat_type=chat_type, chat_id=chat_id)
        elif chat_type == 'c':
            pass
        elif chat_type == 'g':
            pass
        raise Http404