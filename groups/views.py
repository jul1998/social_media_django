from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Groups
from accounts.models import CustomUser
from core.models import Image, Like
import json

    
def get_all_groups(request):
    groups = Groups.objects.all()
    return JsonResponse({"data": [group.serialize() for group in groups]}, safe=False)


def join_group(request):
    if request.method == "POST":
        data = json.loads(request.body)
        
        group_id = data.get("group_id")
        user_id = data.get("user_id")
        
        group = get_object_or_404(Groups, id=group_id)

        if group.members.filter(id=user_id).exists():
            return JsonResponse({"message": "You are already a member of this group"}, status=400)
        
        user = get_object_or_404(CustomUser, id=user_id)
        if not user:
            return JsonResponse({"message": "User not found"})
        
        group.members.add(user)
        return JsonResponse({"message": "You have joined this group"}, status=200)
    return JsonResponse({"message": "Invalid request"}, status=400)


