from django.db import models
from accounts.models import CustomUser

# Create your models here.

class Groups(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    members = models.ManyToManyField(CustomUser, related_name='members', blank=True)
    admins = models.ManyToManyField(CustomUser, related_name='admins', blank=True)
    image = models.ImageField(upload_to='group-images/', blank=True, null=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'members': [member.serialize() for member in self.members.all()],
            'admins': [admin.serialize() for admin in self.admins.all()],
            'image': self.image.url if self.image else '',
            'created_at': self.created_at.strftime('%b %d %Y'),
            'updated_at': self.updated_at.strftime('%b %d %Y'),
        }

    def __str__(self):
        return f"Group: {self.name}"
    
    def get_members(self):
        return self.members.all()
    
    def get_admins(self):
        return self.admins.all()
    

    
