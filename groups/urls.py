from django.urls import path, include
from . import views

urlpatterns = [
    path('all-groups/', views.get_all_groups, name='all_groups'),
]