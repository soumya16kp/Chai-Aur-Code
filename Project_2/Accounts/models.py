# accounts/models.py
from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile/', null=True, blank=True)
    email=models.EmailField(null=True,blank=True)

    def __str__(self):
        return f"{self.user.username}'s profile"




