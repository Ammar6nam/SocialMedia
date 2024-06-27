from django.contrib import admin
from django.urls import path,include
from . import consumers
from .import views
urlpatterns = [
    path('',views.index1,name='chat_index' ),
    path('<slug:slug>/',views.chatroom,name='chatroom'),
]
websocket_urlpatterns = [
    path('ws/<str:room_name>/', consumers.ChatConsumer.as_asgi()),
]