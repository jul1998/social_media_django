from django.shortcuts import render
from django.http import JsonResponse
from .models import Image
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return JsonResponse({'info': 'Django React Course', 'name': 'Rahul'})

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image_file = request.FILES['image']
        user_id = request.POST.get('user_id') 
        description = request.POST.get("description").strip()
        
        # Check if the user exists
        user = User.objects.get(id=user_id)
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