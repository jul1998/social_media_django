from django.contrib import admin

# Register your models here.

from accounts.models import CustomUser

from .models import Image

admin.site.register(Image)
admin.site.register(CustomUser)


