from django.db import models
from django.conf import settings

# Create your models here.

class Profile (models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='users/%Y/%m/%d',blank=True)
    bio=models.TextField(max_length=200,blank=True)
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
    

