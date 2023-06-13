from django.db import models
from accounts.models import CustomUser
from core.models import Image

# Create your models here.

class Notification(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    image = models.ForeignKey(Image, on_delete=models.CASCADE, related_name='notifications')
    content = models.CharField(max_length=100)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.is_seen:
            return f"{self.user.username} saw {self.image.name}"
        else:
            return f"{self.user.username} liked {self.image.name}"
    
    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "image": self.image.name,
            "content": self.content,
            "is_seen": self.is_seen,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    
    class Meta:
        ordering = ['-created_at']
        
