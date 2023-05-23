from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Image(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100, blank=True, null=True) 
    user= models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    description = models.TextField( blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name