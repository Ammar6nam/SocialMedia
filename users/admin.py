from django.contrib import admin
from .models import Profile, Friendship, Follow

# Register your models here.

admin.site.register(Profile)
admin.site.register(Friendship)
admin.site.register(Follow)