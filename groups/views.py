from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Groups
from accounts.models import CustomUser
from core.models import Image, Like
import json

    
def get_all_groups(request):
    groups = Groups.objects.all()
    return JsonResponse({"data": [group.serialize() for group in groups]}, safe=False)
    