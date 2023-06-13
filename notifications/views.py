from django.shortcuts import render
from django.http import JsonResponse
from .models import Notification
from accounts.models import CustomUser
from core.models import Image
import json


# Create your views here.

def notify_when_liked(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get('user_id')
        image_id = data.get('image_id')
        user = CustomUser.objects.get(id=user_id)
        image = Image.objects.get(id=image_id)


        # Check if user exists
        if not user:
            return JsonResponse({'message': 'Invalid user.'}, status=400)
        
        # Check if image exists
        if not image:
            return JsonResponse({'message': 'Invalid image.'}, status=400)
        
        # Check if the user has already liked the image
        if image.likes.filter(id=user_id, image=image_id).exists():
            return JsonResponse({'message': 'Image already liked.'}, status=400)
        
        # Create notification
        notification = Notification.objects.create(
            user=user,
            image=image,
            content=f"{user.username} liked {image.name}"
        )
        notification.save()

        return JsonResponse({'message': 'Notification created successfully.'})
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)
    
