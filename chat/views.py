from django.shortcuts import render
from .models import ChatRoom


def chat_index(request):
    chatrooms = ChatRoom.objects.all()
    return render(request, 'chat/chatindex.html', {'chatrooms': chatrooms})


def chatroom(request, slug):
    chatroom = ChatRoom.objects.get(slug=slug)
    return render(request, 'chat/room.html', {'chatroom':chatroom})