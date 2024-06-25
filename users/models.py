from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)
    bio = models.TextField(max_length=200,blank=True)
    
    # phone_number=models.CharField(max_length=20,blank=True)
    # address=models.CharField(max_length=200,blank=True)
    # city=models.CharField(max_length=100,blank=True)
    # state=models.CharField(max_length=100,blank=True)
    # country=models.CharField(max_length=100,blank=True)
    # zip_code=models.CharField(max_length=10,blank=True)
    # created_at=models.DateTimeField(auto_now_add=True)
    # updated_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username
    

class Friendship(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} is friends with {self.to_user}"

class Follow(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_from')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows_to')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')

    def __str__(self):
        return f"{self.from_user} follows {self.to_user}"