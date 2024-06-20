from django.urls import path
from . import views


urlpatterns = [
    path('create', views.post_create, name='create'),
    path('feed', views.feed, name='feed'),
    path('like', views.like_post, name='like'),
    # path('posts/<int:post_id>/comment/', views.feed, name='add_comment'),
]
