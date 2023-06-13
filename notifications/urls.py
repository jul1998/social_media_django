from django.urls import path, include
from . import views

urlpatterns = [
    path('notify/', views.notify_when_liked, name='notify'), 
]
