from django.urls import path
from . import views


urlpatterns = [
    path('create/',views.post_create,name='create'),
    path('all_posts/',views.posts,name='all_posts'),
    path('like',views.like_post,name='like'),
]
