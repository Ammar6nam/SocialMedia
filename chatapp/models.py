from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name
    
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    message_content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=('date',)

    def __str__(self):
        return self.message_content
    
async def save_message(self, username, room, message):
    user = self.scope['user']
    chat_room = ChatRoom.objects.get(slug=room)
    ChatMessage.objects.create(user=user, room=chat_room, message_content=message)
