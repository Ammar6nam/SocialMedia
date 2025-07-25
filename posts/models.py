from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(default='users/images/post.png', upload_to='images/%y/%m/%d', blank=True)
    caption = models.TextField(blank=True)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, blank=True)
    created = models.DateField(auto_now_add=True)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='posts_liked', blank=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
           self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.CharField(max_length=200)
    created = models.DateField(auto_now_add=True)
    #modified = models.DateField(auto_now=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return f"{self.posted_by.username}: {self.body}"
    # def __str__(self):
    #     return f"{self.user.username}: {self.body}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipients = models.ManyToManyField(User, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
