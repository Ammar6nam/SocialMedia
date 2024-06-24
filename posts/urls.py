from django.urls import path
from . import views


urlpatterns = [
    path('create/', views.post_create, name='create'),
    path('feed/', views.comment_create, name='feed'),
    path('posts/<str:username>/comment/', views.comment_create_userspage, name='comment_create_user'),
    path('like/', views.like_post, name='like'),
    # path('posts/<int:post_id>/comment/', views.feed, name='add_comment'),
]
