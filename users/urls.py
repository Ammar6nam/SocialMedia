from django.urls import path
from users import views
from posts.views import edit_post
from django.contrib.auth import views as auth_view


# urlpatterns = [
#     path('',views.index, name='index'),
#     # path('login/',views.UserLogin.as_view(),name='login')
#     path('login/',views.user_login,name='login'),
#     # path('logout/',auth_view.LogoutView.as_view(template_name='users/logout.html'),name='logout')
#     path('logout/',views.user_logout,name='logout'),
#     path('password_change/',auth_view.PasswordChangeView.as_view(template_name='users/password_change.html'),name='change_password'),
#     path('password_change/done/',auth_view.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'),
#     path('password_reset/',auth_view.PasswordResetView.as_view(template_name='users/password_reset.html'),name='password_reset'),
#     path('password_reset/done/',auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name='password_reset_done'),
#     path('reset/<uidb64>/<token>',auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
#     path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
#     path('register/',views.register,name='register'),
#     # path('register_done/',)
#     path('edit/',views.edit,name='edit'),
# ]

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    # path('userpage/', views.myView, name='userspage'),
    path('users/<str:username>/', views.myView, name='userspage'),
    path('post/<int:post_id>/edit/', edit_post, name='edit_post'),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('password_change/', auth_view.PasswordChangeView.as_view(template_name='users/password_change_form.html'), name='password_change'),
    path('password_change/done/', auth_view.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name= 'users/password_reset_form.html'), name = 'password_reset' ),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_view.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name= 'password_reset_confirm'),
    path('reset/done/', auth_view.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'), name = 'password_reset_complete' ),
    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
    path('friendships/', views.FriendshipListView.as_view(), name='friends_list'),
    path('friendships/create/', views.CreateFriendshipView.as_view(), name='friends_create'),
    path('follows/', views.FollowListView.as_view(), name='follower_list'),
    path('follows/create/', views.CreateFollowView.as_view(), name='follower_create'),
    ]