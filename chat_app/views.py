from django.shortcuts import reverse, render, redirect, Http404
from django.core.exceptions import PermissionDenied
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
            raise PermissionDenied
        context = {
            'chats_list': form_chats_list(request.user),
        }
        return render(request, 'chat/index.html', context)


def get_user_from_chat_id_or_404(chat_id):
    try:
        return User.objects.get(id=chat_id)
    except:
        raise Http404


class OpenChatView(views.View):
    def get(self, request, chat_type, chat_id):
        if chat_type == 'u':
            other_user = get_user_from_chat_id_or_404(chat_id)
            this_chat = ChatModel.objects.get_or_create_user_chat(request.user, other_user)
            chat_messages = MessageModel.objects.filter(chat=this_chat).order_by('datetime')
            context = {
                'other_user': other_user,
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
            other_user = get_user_from_chat_id_or_404(chat_id)
            this_chat = ChatModel.objects.get_or_create_user_chat(request.user, chat_id)
            if request.POST['message']:
                MessageModel.objects.create_new_message(chat=this_chat, content=request.POST['message'], sender=request.user)

            return redirect('chat_app:chat_url', chat_type=chat_type, chat_id=chat_id)
        elif chat_type == 'c':
            pass
        elif chat_type == 'g':
            pass
        raise Http404