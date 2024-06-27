from django import forms
from .models import Post, Comment, Message


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=('title','image','caption')

class PostEditForm(forms.ModelForm):
    class Meta:
        model = Post
        fields=('title','image','caption')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',) 


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']