from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_index, name='chatindex'),
    path('<slug:slug>/', views.chatroom, name='chatroom'),]