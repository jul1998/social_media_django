from django.contrib.auth.models import AbstractUser
from django.db import models
# 


class CustomUser(AbstractUser):
    image = models.ImageField(upload_to='images/', blank=True, null=True, default='')
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField('self', related_name='followers', blank=True)
    following = models.ManyToManyField('self', related_name='following', blank=True)

    def __str__(self):
        return self.username
    
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "image": str(self.image),
            "bio": self.bio,
            "phone": self.phone,
            "address": self.address,
            "followers": [user.username for user in self.followers.all()],
            "following": [user.username for user in self.following.all()],
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "joined_at": self.date_joined
        }