from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Image, Comment, Like
from django.core.files.storage import default_storage
from accounts.models import CustomUser
import json

# Create your views here.

def home(request):
    return JsonResponse({'info': 'Django React Course', 'name': 'Rahul'})

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        user_id = request.POST.get('user_id') 
        description = request.POST.get("description").strip()
        
        # Check if the user exists
        user = CustomUser.objects.get(id=user_id)
        if not user:
            return JsonResponse({'message': 'Invalid user.'}, status=400)
        
        # Check if the description is provided
        if not description:
            description = "No description provided."
        
       # Generate a unique file name
        file_name = default_storage.generate_filename(image_file.name)

        # Save the image file to the desired location
        file_path = default_storage.save(file_name, image_file)

        # Access the URL of the saved image
        image_url = default_storage.url(file_path)

        # Save the image to the database
        try:
            image = Image.objects.create(
                image=image_url,
                name=file_name,
                user=user,
                description=description
            )
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)
        else:
            image.save()
            return JsonResponse({'message': 'Image uploaded successfully.', 'image_url': image_url})

    return JsonResponse({'message': 'Invalid request.'}, status=400)

def get_images(request):
    images = Image.objects.all().order_by('-created_at')
    data = [image.serialize() for image in images]
    return JsonResponse({'data': data})
        

def get_images_by_user_id(request, user_id):
    images = Image.objects.filter(user_id=user_id).order_by('-created_at')
    images_data = [image.serialize() for image in images]
    return JsonResponse({'data': images_data})

import json

def get_comments_by_image(request, image_id):
    comments = Comment.objects.filter(image_id=image_id).order_by('-created_at')
    comments_data = [comment.serialize() for comment in comments]
    return JsonResponse({'data': comments_data})
    


def post_comment(request):
    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
    except Exception as e:
        return JsonResponse({'message': 'Invalid request.'}, status=400)
    else:
        user_id = body.get('user_id')
        image_id = body.get('image_id')
        content = body.get('content')
        user = CustomUser.objects.get(id=user_id)
        image = Image.objects.get(id=image_id)
        comment = Comment.objects.create(
            user=user,
            image=image,
            content=content
        )
        comment.save()
        return JsonResponse({'message': 'Comment posted successfully.'})
        

def like_image(request):
    body_unicode = request.body.decode('utf-8')
    try:
        body = json.loads(body_unicode)
        
    except Exception as e:
        return JsonResponse({'message': 'Invalid Request.'}, status=400)
    else: 

        user_id = body.get('user_id')
        image_id = body.get('image_id')
        user = get_object_or_404(CustomUser, id=user_id)
        image = get_object_or_404(Image, id=image_id)

        # Check if the user has already liked the image
        existing_like = Like.objects.filter(user=user, image=image)
        if existing_like.exists():
            # Remove like
            existing_like.delete()

            return JsonResponse({'message': 'Image like already liked.'})
        
        like = Like.objects.create(
            user=user,
            image=image
        )
        like.save()
        return JsonResponse({'message': 'Image liked successfully.'})

def get_likes_by_image(request, image_id):
    likes = Like.objects.filter(image_id=image_id)
    likes_data =[like.serialize() for like in likes]
    return JsonResponse({'data': likes_data})

