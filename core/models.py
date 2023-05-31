from django.db import models
from accounts.models import CustomUser
from django.db.models.signals import post_save

# Create your models here.

class Comment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comment')
    image = models.ForeignKey('Image', on_delete=models.CASCADE, related_name='comment')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} commented on {self.image.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "image": self.image.name,
            "content": self.content,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    class Meta:
        ordering = ['-created_at']

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100, blank=True, null=True) 
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='images')
    description = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(CustomUser, related_name='likes', blank=True)
    comments = models.ManyToManyField(Comment, related_name='commented_images', blank=True)

    
    def __str__(self):
        return self.name
    
    def serialize(self):
        return {
            "id": self.id,
            "image": str(self.image),
            "name": self.name,
            "user": self.user.username if self.user else None,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
