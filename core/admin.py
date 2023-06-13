from django.contrib import admin

# Register your models here.

from accounts.models import CustomUser

from .models import Image, Comment, Like 

admin.site.register(Image)
admin.site.register(CustomUser)
admin.site.register(Comment)
admin.site.register(Like)


