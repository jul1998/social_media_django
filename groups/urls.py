from django.urls import path, include
from . import views

urlpatterns = [
    path('all-groups/', views.get_all_groups, name='all_groups'),
    path('join-group/', views.join_group, name='join_group'),
    path('leave-group/', views.leave_group, name='leave_group'),
]