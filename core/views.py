from django.shortcuts import render
from django.http import JsonResponse
from .models import Image, Comment
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
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

def get_comments_by_image(request):

    body_unicode = request.body.decode('utf-8')
    print("body_unicode", request)
    print("request.body", request.body)
    try:
        body = json.loads(body_unicode)
    except Exception as e:
        print("Error", e)
        return JsonResponse({'message': 'Invalid request.'}, status=400)
    else:

        image_id = body.get('image_id')
        print("image_id", image_id)
        comments = Comment.objects.filter(image_id=image_id).order_by('-created_at')
        comments_data = [comment.serialize() for comment in comments]
        return JsonResponse({'data': comments_data})



