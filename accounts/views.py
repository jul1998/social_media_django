from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
import jwt
from datetime import datetime, timedelta
from .models import CustomUser

def create_auth_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(hours=1), # token will expire in 1 hour
        'iat': datetime.utcnow()
    }
    secret = 'your_secret_key_here'
    token = jwt.encode(payload, secret, algorithm='HS256')
    print(token)
    return token




def register(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username')
        email = body.get('email')
        password = body.get('password')
        bio=body.get('bio')
        phone=body.get('phone')
        address=body.get('address')
        first_name=body.get('first_name')
        last_name=body.get('last_name')
        image=body.get('image')

        print(username, email, password)
        if not all([username, email, password]):
            return JsonResponse({'msg': 'Please fill all fields'}, status=400)
        
        try:
            user = CustomUser.objects.create_user(username=username, email=email, password=password, bio=bio, phone=phone, address=address, first_name=first_name, last_name=last_name, image=image)
            user.save()
            login(request, user)
            return JsonResponse({'msg': 'User created successfully'}, status=201)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400) 
    else:
        return JsonResponse({"msg": "Method not allowed"}, status=400)
    

def logout_view(request):
    logout(request)
    return JsonResponse({"success": True,'msg': 'Logout successful'}, status=200)


def login_view(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        username = body.get('username')
        password = body.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            response = JsonResponse({'msg': 'Login successful', 'user_id': user.id, "success": True, "token":create_auth_token(user.id) }, status=200)
            response.set_cookie('auth_token', create_auth_token(user.id), httponly=True, secure=False, samesite='None')    
            return response 
        else:
            return JsonResponse({'msg': 'Invalid credentials'}, status=400)
    else:
        errors = "An error occurred"
        return JsonResponse({'msg': 'Invalid form data', 'errors': errors}, status=400)


def get_profile_info(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return JsonResponse({'data': user.serialize()})
