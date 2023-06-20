from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Notification
from accounts.models import CustomUser
from core.models import Image, Like
import json


# Create your views here.

def notify_when_liked(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_id = data.get('user_id')
        image_id = data.get('image_id')
        user = CustomUser.objects.get(id=user_id)
        image = Image.objects.get(id=image_id)
        like = Like.objects.filter(user=user, image=image)
        notification = Notification.objects.filter(user=user, image=image).first()  # Retrieve the first notification instance
        print(notification)


        # Check if user exists
        if not user:
            return JsonResponse({'message': 'Invalid user.'}, status=400)
        
        # Check if image exists
        if not image:
            return JsonResponse({'message': 'Invalid image.'}, status=400)
        
        # Check if notification exists and is not seen yet
        if notification and not notification.is_seen:
            return JsonResponse({'message': 'Notification already exists.'})


        
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
    
def get_notifications(request, user_id):
    if request.method == "GET":
        user = get_object_or_404(CustomUser, id=user_id)
        
        # Check if user exists
        if not user:
            return JsonResponse({'message': 'Invalid user.'}, status=400)
        
        notifications = user.notifications.all()
        return JsonResponse([notification.serialize() for notification in notifications], safe=False)
    else:
        return JsonResponse({'message': 'Invalid request.'}, status=400)
    

def show_not_seen_notifications(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    notifications = Notification.objects.filter(user=user, is_seen=False)
    notifications_data = [notification.serialize() for notification in notifications]
    return JsonResponse({"data": notifications_data}, safe=False)

def set_notification_seen(request):
    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
    except Exception as e:
        return JsonResponse({'message': 'Invalid request.'}, status=400)
    else:
        notification_id = body.get('notification_id')
        notification = get_object_or_404(Notification, id=notification_id)
        
        if notification.is_seen:
            return JsonResponse({'message': 'Notification already seen.'})
        
        notification.is_seen = True
        notification.save()
        return JsonResponse({'message': 'Notification seen.'})